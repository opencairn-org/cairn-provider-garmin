"""Raw-blob archival and claim-check upload against a fake presign RPC and HTTP."""

import asyncio
import json
from dataclasses import dataclass
from typing import Any

import pytest
import requests

from cairn_garmin import archive
from cairn_garmin import config as C
from tests.fakes import FakeNC, as_nats

PRESIGN = {"url": "https://s3.example/put", "blob_id": "raw/garmin/1.json", "required_headers": {"X-A": "1"}}


@dataclass
class Resp:
    status_code: int
    content: bytes = b""


class HTTP:
    """Stands in for requests.request/get; records calls, returns queued responses."""

    def __init__(self, *responses: Resp | Exception) -> None:
        self.responses = list(responses)
        self.calls: list[tuple[str, str, dict[str, Any]]] = []

    def _next(self) -> Resp:
        r = self.responses.pop(0)
        if isinstance(r, Exception):
            raise r
        return r

    def request(self, method: str, url: str, **kw: Any) -> Resp:
        self.calls.append((method, url, kw))
        return self._next()

    def get(self, url: str, **kw: Any) -> Resp:
        self.calls.append(("GET", url, kw))
        return self._next()


@pytest.fixture
def http(monkeypatch: pytest.MonkeyPatch) -> HTTP:
    h = HTTP()
    monkeypatch.setattr(requests, "request", h.request)
    monkeypatch.setattr(requests, "get", h.get)
    return h


def test_archive_uploads_envelope(http: HTTP) -> None:
    http.responses = [Resp(200)]
    nc = FakeNC({archive.PRESIGN_SUBJECT: PRESIGN})
    env_in = archive.envelope({"activityId": 42}, None, [{"uuid": "g1"}])
    blob_id, size = asyncio.run(archive.archive(as_nats(nc), "u1", "42", env_in))

    assert blob_id == "raw/garmin/1.json"
    method, url, kw = http.calls[0]
    assert (method, url) == ("PUT", "https://s3.example/put")
    assert kw["headers"] == {"X-A": "1", "Content-Type": "application/json"}
    assert size == len(kw["data"])
    env = json.loads(kw["data"])
    assert env["activity"] == {"activityId": 42}
    assert env["gear"] == [{"uuid": "g1"}]
    assert env["version"] == C.DATASET_VERSION
    assert env["provenance"]["provider"] == C.PROVIDER
    assert env["provenance"]["worker_version"] == C.VERSION
    assert nc.requests[0][1]["content_length"] == size


@pytest.mark.parametrize(
    ("reply", "responses"),
    [
        (RuntimeError("no responders"), []),
        ({"error": "quota"}, []),
        (PRESIGN, [OSError("connection reset")]),
        (PRESIGN, [Resp(403)]),
    ],
)
def test_archive_is_best_effort(
    http: HTTP, reply: dict[str, Any] | Exception, responses: list[Resp | Exception]
) -> None:
    http.responses = list(responses)  # the param list is shared between runs
    nc = FakeNC({archive.PRESIGN_SUBJECT: reply})
    assert asyncio.run(archive.archive(as_nats(nc), "u1", "42", archive.envelope({}, {}, None))) == (None, 0)


def test_upload_result_returns_ref(http: HTTP) -> None:
    http.responses = [Resp(201)]
    nc = FakeNC({archive.PRESIGN_SUBJECT: {**PRESIGN, "blob_id": "transfer/x.json"}})
    ref = asyncio.run(archive.upload_result(as_nats(nc), b"{}"))

    assert ref["blob_id"] == "transfer/x.json"
    assert ref["size"] == 2
    assert nc.requests[0][1]["kind"] == "result"
    assert nc.requests[0][1]["content_sha256"] == ref["sha256"]


@pytest.mark.parametrize(
    ("reply", "responses"),
    [({"error": "denied"}, []), (PRESIGN, [Resp(500)])],
)
def test_upload_result_raises(http: HTTP, reply: dict[str, Any], responses: list[Resp | Exception]) -> None:
    http.responses = list(responses)  # the param list is shared between runs
    nc = FakeNC({archive.PRESIGN_SUBJECT: reply})
    with pytest.raises(RuntimeError):
        asyncio.run(archive.upload_result(as_nats(nc), b"{}"))


def test_fetch_uses_given_url(http: HTTP) -> None:
    http.responses = [Resp(200, b'{"activity": {"activityId": 1}}')]
    env = asyncio.run(archive.fetch(as_nats(FakeNC()), "https://s3.example/get", "raw/1.json"))
    assert env == {"activity": {"activityId": 1}}


def test_fetch_represigns_expired_url(http: HTTP) -> None:
    http.responses = [Resp(403), Resp(200, b"{}")]
    nc = FakeNC({C.PRESIGN_DOWNLOAD_SUBJECT: {"url": "https://s3.example/fresh"}})
    assert asyncio.run(archive.fetch(as_nats(nc), "https://s3.example/old", "raw/1.json")) == {}
    assert http.calls[1][1] == "https://s3.example/fresh"
    assert nc.requests == [(C.PRESIGN_DOWNLOAD_SUBJECT, {"blob_id": "raw/1.json"})]


def test_fetch_represigns_after_get_error(http: HTTP) -> None:
    http.responses = [OSError("dns"), Resp(200, b"{}")]
    nc = FakeNC({C.PRESIGN_DOWNLOAD_SUBJECT: {"url": "https://s3.example/fresh"}})
    assert asyncio.run(archive.fetch(as_nats(nc), "https://s3.example/old", "raw/1.json")) == {}


@pytest.mark.parametrize(
    ("url", "fallback", "replies", "responses"),
    [
        ("", "", {}, []),  # nothing to download
        ("", "raw/1.json", {}, []),  # presign RPC times out
        ("", "raw/1.json", {C.PRESIGN_DOWNLOAD_SUBJECT: {"error": "gone"}}, []),
        ("https://s3.example/get", "", {}, [Resp(404)]),
        ("https://s3.example/get", "", {}, [Resp(200, b"[]")]),  # not an envelope
    ],
)
def test_fetch_failures(
    http: HTTP,
    url: str,
    fallback: str,
    replies: dict[str, dict[str, Any] | Exception],
    responses: list[Resp | Exception],
) -> None:
    http.responses = list(responses)  # the param list is shared between runs
    with pytest.raises((RuntimeError, TypeError)):
        asyncio.run(archive.fetch(as_nats(FakeNC(replies)), url, fallback))
