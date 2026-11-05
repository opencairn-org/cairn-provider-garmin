"""Garmin handlers end to end against the SDK's NATS/JetStream fakes. The
runtime itself (consumers, settlement, presence, claim-check, failure
envelopes, release rules) is tested in cairn-provider-sdk."""

import asyncio
import json
from datetime import UTC, datetime
from typing import Any, cast

import pytest
from cairn.v1 import activity_pb2 as a
from cairn.v1 import gear_pb2 as g
from cairn.worker.v1 import worker_service_pb2 as w
from cairn_provider_sdk import Job, ParserTooOldError, TerminalJobError, archive
from cairn_provider_sdk.archive import ResultRef
from google.protobuf import json_format

from cairn_garmin import config as C
from cairn_garmin import mapping, runtime
from tests.fakes import FakeJS, FakeKV, FakeNC, Responder, make_worker

START_MS = 1_700_000_000_000


class FakeClient:
    def __init__(self) -> None:
        self.days: list[str] = []

    def list_activities(self, start: int, limit: int) -> list[dict[str, Any]]:
        if start:
            return []
        return [{"activityId": 7, "beginTimestamp": START_MS}, {"activityName": "no id"}]

    def get_activity(self, ext_id: str) -> dict[str, Any]:
        return {"activityId": ext_id, "beginTimestamp": START_MS, "activityType": {"typeKey": "running"}}

    def get_activity_details(self, ext_id: str) -> dict[str, Any]:
        return {
            "metricDescriptors": [
                {"key": "directTimestamp", "metricsIndex": 0},
                {"key": "sumDistance", "metricsIndex": 1},
            ],
            "activityDetailMetrics": [{"metrics": [START_MS, 0.0]}, {"metrics": [START_MS + 1000, 3.0]}],
        }

    def daily_health(self, day: str) -> dict[str, float]:
        self.days.append(day)
        return {"Steps": 100.0}

    # gear-service shapes (anonymised)
    def activity_gear(self, ext_id: str) -> list[dict[str, Any]]:
        return [GEAR_BIKE]

    def gear(self) -> list[dict[str, Any]]:
        return [GEAR_BIKE, GEAR_SHOES]

    def gear_defaults(self) -> list[dict[str, Any]]:
        return [{"uuid": GEAR_SHOES["uuid"], "activityTypeKey": "running", "defaultGear": True}]


GEAR_BIKE: dict[str, Any] = {
    "uuid": "aaaa-1",
    "gearTypeName": "Bike",
    "gearStatusName": "active",
    "displayName": "Canyon",
    "gearMakeName": "Canyon",
    "gearModelName": "Grail",
    "totalDistance": 1500.5,
}
GEAR_SHOES: dict[str, Any] = {
    "uuid": "bbbb-2",
    "gearTypeName": "Shoes",
    "gearStatusName": "retired",
    "customMakeModel": "Pegasus",
}


def job(**d: Any) -> Job:
    return Job.of(d)


def discover(wk: runtime.Worker, req: dict[str, Any]) -> dict[str, Any]:
    msg = Responder(json.dumps(req).encode())
    asyncio.run(wk._on_discover(cast(Any, msg)))
    return msg.response


def results(js: FakeJS, subject: str) -> list[w.JobResult]:
    return [json_format.Parse(d, w.JobResult()) for s, d, _ in js.published if s == subject]


@pytest.fixture
def uploads(monkeypatch: pytest.MonkeyPatch) -> list[bytes]:
    """Captures claim-check uploads; the raw archive is a no-op returning a blob id."""
    bodies: list[bytes] = []

    async def fake_upload(nc: object, provider: str, body: bytes) -> ResultRef:
        bodies.append(body)
        return {"blob_id": f"transfer/{len(bodies)}", "size": len(body), "sha256": "x"}

    async def fake_archive(nc: object, provider: str, *args: Any) -> tuple[str | None, int]:
        return "raw/7.json", 99

    monkeypatch.setattr(archive, "upload_result", fake_upload)
    monkeypatch.setattr(archive, "archive", fake_archive)
    return bodies


def test_identity_and_subjects() -> None:
    assert C.IDENTITY.worker_name == C.WORKER_NAME
    assert f"cairn.jobs.fetch_source.garmin.{C.WORKER_NAME}" == C.SUBJ_FETCH
    assert f"cairn.results.reconcile.garmin.{C.WORKER_NAME}" == C.RESULT_RECONCILE_PREFIX
    assert f"cairn.discover.garmin.{C.WORKER_NAME}" == C.DISCOVER_SUBJECT
    wk, _ = make_worker()
    assert set(wk.jobs) == {"fetch_source", "import_metrics", "parse_blob", "reconcile", "import_gear"}


def test_discover_lists_a_page() -> None:
    wk, _ = make_worker(FakeClient())
    resp = discover(wk, {"account_id": "acc-1", "start_page": 1})
    assert resp["next_page"] == 2
    assert resp["items"] == [
        {
            "item_type": "activity",
            "external_id": "7",
            "item_time": datetime.fromtimestamp(START_MS / 1000, UTC).isoformat(),
        }
    ]
    assert discover(wk, {"account_id": "acc-1", "start_page": 2}) == {"items": [], "complete": True}


def test_discover_reports_errors() -> None:
    wk, _ = make_worker()  # no client, no creds
    assert "no Garmin credentials" in discover(wk, {"account_id": "acc-9"})["error"]


def test_creds_come_from_the_server() -> None:
    nc = FakeNC({C.CREDS_SUBJECT: {"email": "a@b", "password": "pw"}})
    wk, _ = make_worker(nc=nc)
    client = asyncio.run(wk._client_for("acc-2"))
    assert client._email == "a@b"
    assert client._garth_home == "/nonexistent/acc-2"
    assert asyncio.run(wk._client_for("acc-2")) is client  # cached
    assert len(nc.requests) == 1


@pytest.mark.parametrize("reply", [{"error": "revoked"}, RuntimeError("no responders")])
def test_creds_fall_back_to_env(reply: dict[str, Any] | Exception) -> None:
    cfg = C.Config(garmin_email="dev@b", garmin_password="pw", garth_home="/t")
    wk, _ = make_worker(nc=FakeNC({C.CREDS_SUBJECT: reply}), cfg=cfg)
    assert asyncio.run(wk._fetch_creds("acc-3")) == ("dev@b", "pw")


def test_fetch_source_publishes_activity_with_stream(uploads: list[bytes]) -> None:
    wk, js = make_worker(FakeClient())
    asyncio.run(wk._handle_fetch_source(job(ext_id="7", account_id="acc-1", user_id="u1", fetch_streams=True)))

    (env,) = results(js, C.RESULT_SUBJECT)
    assert env.payload_ref.blob_id == "transfer/1"
    assert (env.worker_name, env.worker_version, env.worker_package) == (C.WORKER_NAME, C.VERSION, C.PACKAGE)
    full = json_format.Parse(uploads[0], w.JobResult())
    act = full.events[-1].activity  # the GEAR event precedes it
    assert act.ref.external_id == "7"
    assert act.raw_blob_id == "raw/7.json"
    assert list(act.stream.distance_m) == [0.0, 3.0]


def test_fetch_source_carries_gear(uploads: list[bytes]) -> None:
    wk, _ = make_worker(FakeClient())
    asyncio.run(wk._handle_fetch_source(job(account_id="acc-1", user_id="u1", ext_id="7")))
    events = json_format.Parse(uploads[0], w.JobResult()).events
    assert [e.type for e in events] == [w.WORKER_EVENT_TYPE_GEAR, w.WORKER_EVENT_TYPE_ACTIVITY]
    gear = events[0].gear
    assert gear.ref.external_id == "aaaa-1"
    assert gear.ref.external_account_id == "acc-1"
    assert gear.payload.kind == g.GEAR_KIND_BIKE
    assert gear.payload.name == "Canyon"
    assert events[1].activity.payload.gear_external_id == "aaaa-1"
    assert events[1].activity.payload.gear_name == "Canyon"


def test_fetch_source_gear_is_optional(uploads: list[bytes]) -> None:
    class Broken(FakeClient):
        def activity_gear(self, ext_id: str) -> list[dict[str, Any]]:
            raise RuntimeError("garmin 429")

    wk, _ = make_worker(Broken())
    asyncio.run(wk._handle_fetch_source(job(account_id="acc-1", ext_id="7")))
    events = json_format.Parse(uploads[0], w.JobResult()).events
    assert [e.type for e in events] == [w.WORKER_EVENT_TYPE_ACTIVITY]
    assert events[0].activity.payload.gear_external_id == ""


def test_fetch_source_gear_lookup_can_be_disabled(uploads: list[bytes]) -> None:
    cfg = C.Config(garmin_email="", garmin_password="", garth_home="/nonexistent", fetch_activity_gear=False)
    wk, _ = make_worker(FakeClient(), cfg=cfg)
    asyncio.run(wk._handle_fetch_source(job(account_id="acc-1", ext_id="7")))
    events = json_format.Parse(uploads[0], w.JobResult()).events
    assert len(events) == 1
    assert events[0].activity.payload.gear_external_id == ""


def test_import_gear_publishes_list_with_defaults(uploads: list[bytes]) -> None:
    wk, js = make_worker(FakeClient())
    asyncio.run(wk._handle_import_gear(job(account_id="acc-1", user_id="u1")))
    assert js.published[-1][0] == C.RESULT_GEAR
    events = json_format.Parse(uploads[0], w.JobResult()).events
    by_id = {e.gear.ref.external_id: e.gear.payload for e in events}
    assert set(by_id) == {"aaaa-1", "bbbb-2"}
    assert by_id["aaaa-1"].brand == "Canyon"
    assert by_id["aaaa-1"].model == "Grail"
    assert by_id["aaaa-1"].distance_m == 1500.5
    shoes = by_id["bbbb-2"]
    assert shoes.kind == g.GEAR_KIND_SHOE
    assert shoes.retired
    assert shoes.name == "Pegasus"
    assert list(shoes.default_for) == [a.ACTIVITY_TYPE_RUN]
    assert shoes.primary


def test_import_gear_without_gear_publishes_nothing() -> None:
    class Empty(FakeClient):
        def gear(self) -> list[dict[str, Any]]:
            return []

    wk, js = make_worker(Empty())
    asyncio.run(wk._handle_import_gear(job(account_id="acc-1")))
    assert js.published == []


def test_import_gear_defaults_are_optional(uploads: list[bytes]) -> None:
    class NoDefaults(FakeClient):
        def gear_defaults(self) -> list[dict[str, Any]]:
            raise RuntimeError("garmin 500")

    wk, _ = make_worker(NoDefaults())
    asyncio.run(wk._handle_import_gear(job(account_id="acc-1", user_id="u1")))
    events = json_format.Parse(uploads[0], w.JobResult()).events
    assert all(not list(e.gear.payload.default_for) for e in events)


def test_fetch_source_requires_ext_id() -> None:
    wk, _ = make_worker(FakeClient())
    with pytest.raises(ValueError, match="ext_id"):
        asyncio.run(wk._handle_fetch_source(job()))


def test_parse_blob_remaps_archived_envelope(uploads: list[bytes], monkeypatch: pytest.MonkeyPatch) -> None:
    client = FakeClient()

    async def fake_fetch(nc: object, provider: str, url: str, fallback: str) -> dict[str, Any]:
        return {"version": 1, "activity": client.get_activity("7"), "details": client.get_activity_details("7")}

    monkeypatch.setattr(archive, "fetch", fake_fetch)
    wk, _ = make_worker()
    asyncio.run(
        wk._handle_parse_blob(
            job(ext_id="7", user_id="u1", blob={"url": "https://s3/x", "fallback_handle": "raw/7.json"})
        )
    )

    act = json_format.Parse(uploads[0], w.JobResult()).events[0].activity
    assert act.raw_blob_id == "raw/7.json"
    assert act.stream.sample_count == 2


def test_import_metrics_emits_one_event_per_day(uploads: list[bytes]) -> None:
    client = FakeClient()
    wk, _ = make_worker(client)
    day = 86_400
    asyncio.run(wk._handle_import_metrics(job(account_id="acc-1", user_id="u1", since_unix=0, until_unix=2 * day)))

    assert client.days == ["1970-01-01", "1970-01-02", "1970-01-03"]
    events = json_format.Parse(uploads[0], w.JobResult()).events
    assert [e.metric.key for e in events] == ["Steps"] * 3


def test_import_metrics_without_data_publishes_nothing() -> None:
    class Empty(FakeClient):
        def daily_health(self, day: str) -> dict[str, float]:
            return {}

    wk, js = make_worker(Empty())
    asyncio.run(wk._handle_import_metrics(job(account_id="acc-1")))
    assert js.published == []


def test_manifest_declares_provider_meta() -> None:
    wk, js = make_worker()
    js.kv = FakeKV()
    asyncio.run(wk.publish_manifest())
    ((key, payload),) = js.kv.puts
    assert key == C.WORKER_NAME
    assert payload["provider"] == C.PROVIDER
    assert payload["package"] == C.PACKAGE
    assert payload["version"] == C.VERSION
    meta = payload["provider_meta"]
    assert meta["auth_method"] == "credentials"
    assert "oauth" not in meta
    assert [f["key"] for f in meta["config_fields"]] == ["client_id", "client_secret"]
    assert meta["config_fields"][1]["secret"] is True


def test_presence_advertises_health_capabilities() -> None:
    wk, _ = make_worker()
    payload = wk.presence_payload()
    assert payload["capabilities"]["HRV"]["read"] is True
    assert payload["capabilities"]["Gear"]["granularity"] == "per-account"
    assert payload["worker_key"] == f"{C.WORKER_NAME}-garmin"
    assert payload["webhooks"] is False


def test_envelope_holds_every_parser_input() -> None:
    env = mapping.envelope({"activityId": 42}, None, [{"uuid": "g1"}])
    assert list(env) == ["version", "provenance", "activity", "details", "gear"]
    assert env["version"] == C.DATASET_VERSION
    assert env["provenance"]["provider"] == C.PROVIDER
    assert env["provenance"]["worker_version"] == C.VERSION
    assert env["provenance"]["package"] == C.PACKAGE
    assert env["gear"] == [{"uuid": "g1"}]


def test_fetch_source_archives_what_it_parsed(uploads: list[bytes], monkeypatch: pytest.MonkeyPatch) -> None:
    archived: list[dict[str, Any]] = []

    async def capture(
        nc: object, provider: str, user_id: str, source_id: str, env: dict[str, Any]
    ) -> tuple[str | None, int]:
        archived.append(env)
        return "raw/7.json", 99

    monkeypatch.setattr(archive, "archive", capture)
    wk, _ = make_worker(FakeClient())
    asyncio.run(wk._handle_fetch_source(job(account_id="acc-1", user_id="u1", ext_id="7")))
    (env,) = archived
    assert env["version"] == C.DATASET_VERSION
    assert env["gear"] == [GEAR_BIKE]
    # Re-parsing the archive reproduces the import.
    reparsed = mapping.parse_archive(env, user_id="u1", account_id="acc-1", ext_id="7", blob_id="raw/7.json")
    imported = json_format.Parse(uploads[0], w.JobResult()).events
    # Blob metadata is the upload's, not parser output; core keeps it on re-parse.
    imported[-1].activity.ClearField("raw_content_type")
    imported[-1].activity.ClearField("raw_size_bytes")
    assert [json_format.MessageToDict(e) for e in reparsed] == [json_format.MessageToDict(e) for e in imported]


def test_parse_blob_reads_archived_gear(uploads: list[bytes], monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_fetch(nc: object, provider: str, url: str, fallback: str) -> dict[str, Any]:
        return {"version": 1, "activity": FakeClient().get_activity("7"), "gear": [GEAR_BIKE]}

    monkeypatch.setattr(archive, "fetch", fake_fetch)
    wk, _ = make_worker()
    asyncio.run(
        wk._handle_parse_blob(job(ext_id="7", user_id="u1", account_id="acc-1", blob={"fallback_handle": "raw/7.json"}))
    )
    events = json_format.Parse(uploads[0], w.JobResult()).events
    assert [e.type for e in events] == [w.WORKER_EVENT_TYPE_GEAR, w.WORKER_EVENT_TYPE_ACTIVITY]
    assert events[1].activity.payload.gear_external_id == "aaaa-1"


def test_parse_blob_version_guards(uploads: list[bytes], monkeypatch: pytest.MonkeyPatch) -> None:
    async def future(nc: object, provider: str, url: str, fallback: str) -> dict[str, Any]:
        return {"version": C.DATASET_VERSION + 1, "activity": {}}

    monkeypatch.setattr(archive, "fetch", future)
    wk, _ = make_worker()
    with pytest.raises(ParserTooOldError):
        asyncio.run(wk._handle_parse_blob(job(min_parser_version="1.99")))
    with pytest.raises(TerminalJobError):
        asyncio.run(wk._handle_parse_blob(job(blob={})))
    assert uploads == []


def test_parse_archive_marks_gear_unknown_when_not_looked_up() -> None:
    act = FakeClient().get_activity("7")
    unknown = mapping.parse_archive(
        {"version": 1, "activity": act, "gear": None}, user_id="u1", account_id="a1", ext_id="7"
    )
    legacy = mapping.parse_archive({"version": 1, "activity": act}, user_id="u1", account_id="a1", ext_id="7")
    none = mapping.parse_archive({"version": 1, "activity": act, "gear": []}, user_id="u1", account_id="a1", ext_id="7")
    assert unknown[-1].activity.payload.gear_unknown is True
    assert legacy[-1].activity.payload.gear_unknown is True
    assert none[-1].activity.payload.gear_unknown is False
