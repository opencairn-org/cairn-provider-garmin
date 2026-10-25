"""Claim-check publish path: event-carrying results spill to the blob store
and publish a payload_ref envelope; terminal failures publish a failure
envelope so the server fails the queue item with the true reason."""

import asyncio
import hashlib
import json

import pytest
from google.protobuf import json_format

import cairn_garmin  # noqa: F401 (proto path bootstrap)
from cairn.worker.v1 import worker_service_pb2 as w
from cairn_garmin import archive
from tests.fakes import make_worker


def test_publish_result_claim_checks_events(monkeypatch: pytest.MonkeyPatch) -> None:
    wk, js = make_worker()
    uploaded: dict[str, bytes] = {}

    async def fake_upload(nc: object, body: bytes) -> archive.ResultRef:
        uploaded["body"] = body
        return {"blob_id": "transfer/garmin/x.json", "size": len(body), "sha256": hashlib.sha256(body).hexdigest()}

    monkeypatch.setattr(archive, "upload_result", fake_upload)

    jr = w.JobResult(
        worker_name="garmin-fetcher",
        events=[w.WorkerEvent(type=w.WORKER_EVENT_TYPE_ACTIVITY)],
    )
    asyncio.run(wk._publish_result("cairn.results.fetch_source.garmin.garmin-fetcher", jr))

    ((subject, data, _),) = js.published
    assert subject == "cairn.results.fetch_source.garmin.garmin-fetcher"
    env = json_format.Parse(data, w.JobResult())
    assert env.payload_ref.blob_id == "transfer/garmin/x.json"
    assert env.payload_ref.size_bytes == len(uploaded["body"])
    assert not env.events

    full = json_format.Parse(uploaded["body"], w.JobResult())
    assert len(full.events) == 1


def test_publish_result_inline_when_no_events() -> None:
    wk, js = make_worker()
    jr = w.JobResult(worker_name="garmin-fetcher")
    asyncio.run(wk._publish_result("cairn.results.fetch_source.garmin.garmin-fetcher", jr))

    ((_, data, _),) = js.published
    env = json_format.Parse(data, w.JobResult())
    assert not env.HasField("payload_ref")


def test_publish_failure_envelope() -> None:
    wk, js = make_worker()
    body = json.dumps({"ext_id": "99", "account_id": "a1", "user_id": "u1"}).encode()
    asyncio.run(wk._publish_failure("cairn.jobs.fetch_source.garmin.garmin-fetcher", body, RuntimeError("boom")))

    ((subject, data, _),) = js.published
    assert subject == "cairn.results.fetch_source.garmin.garmin-fetcher"
    env = json_format.Parse(data, w.JobResult())
    assert env.failed_ref.external_id == "99"
    assert env.failed_ref.external_account_id == "a1"
    assert env.error.message == "boom"
    assert env.error.code == "RuntimeError"
