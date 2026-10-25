"""The worker's real NATS operations against a nats-server that grants exactly
cairn-core's StandardPermissionTemplate, so a subject the template lacks fails
here instead of in production. Runs twice: a static user carrying the template,
and core's auth-callout flow (enrollment token -> user JWT) with a test responder."""

import asyncio
import base64
import hashlib
import json
import logging
import os
import shutil
import socket
import subprocess
import threading
import time
from collections.abc import Awaitable, Callable, Iterator
from dataclasses import dataclass, field
from datetime import UTC, datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, ClassVar, cast

import nats
import nkeys
import pytest
from nats.aio.client import Client as NATS
from nats.aio.msg import Msg
from nats.js.api import RetentionPolicy, StreamConfig

from cairn_garmin import config as C
from cairn_garmin import runtime
from cairn_garmin.garmin_client import GarminClient

PROVIDER = C.PROVIDER
WORKER_KEY = f"{C.WORKER_NAME}-{PROVIDER}"
ACCOUNT = "acc-1"
JOB_STREAM, WEBHOOK_STREAM = "CAIRN_JOBS", "CAIRN_WEBHOOKS"
BUCKETS = ["cairn_worker_presence", "cairn_worker_manifests", "cairn_rate_limits"]
TOKEN, BAD_TOKEN = "enroll-garmin", "wrong"


def standard_template(p: str, name: str) -> tuple[list[str], list[str]]:
    """Mirror of cairn-core domain.StandardPermissionTemplate(p, name); keep in sync."""
    wk = f"{name}-{p}"
    kinds = ("fetch_source", "parse_blob", "backfill", "reconcile", "import_metrics", "import_gear")
    jobs = [f"cairn.jobs.{t}.{p}.{name}" for t in kinds] + [f"cairn.jobs.{t}.{p}" for t in kinds]  # + legacy drain
    webhook = f"cairn.webhooks.{wk}.event"
    js = ["$JS.API.STREAM.NAMES"]
    js += [f"$JS.API.CONSUMER.CREATE.{JOB_STREAM}.*.{f}" for f in jobs]
    js += [f"$JS.API.CONSUMER.DURABLE.CREATE.{JOB_STREAM}.*", f"$JS.API.CONSUMER.CREATE.{WEBHOOK_STREAM}.*.{webhook}"]
    for st in (JOB_STREAM, WEBHOOK_STREAM):
        js += [f"$JS.API.CONSUMER.INFO.{st}.*", f"$JS.API.CONSUMER.MSG.NEXT.{st}.*", f"$JS.ACK.{st}.>"]
    for b in BUCKETS:
        js += [f"$JS.API.STREAM.INFO.KV_{b}", f"$JS.API.DIRECT.GET.KV_{b}.>", f"$JS.API.STREAM.MSG.GET.KV_{b}"]
        js += [f"$KV.{b}.>"]
    js += [
        "$JS.API.STREAM.INFO.KV_cairn_core",
        "$JS.API.DIRECT.GET.KV_cairn_core.>",
        "$JS.API.STREAM.MSG.GET.KV_cairn_core",
    ]
    publish = [
        f"cairn.results.fetch_source.{p}",
        f"cairn.results.parse_blob.{p}",
        f"cairn.results.backfill.{p}",
        f"cairn.results.reconcile.{p}.*",
        f"cairn.results.import_metrics.{p}",
        f"cairn.results.import_gear.{p}",
        f"cairn.jobs.fetch_source.{p}.{name}",
        f"cairn.workers.{wk}.>",
        f"cairn.tokens.{p}.>",
        f"cairn.creds.{p}.get",
        f"cairn.blobs.presign_upload.{p}",
        f"cairn.blobs.presign_download.{p}",
        "cairn.accounts.lookup_by_provider_ext",
        "_INBOX.>",
        *js,
    ]
    subscribe = [
        *jobs,
        f"cairn.cmd.worker.{wk}.>",
        f"cairn.discover.{p}.{name}",
        webhook,
        f"cairn.webhooks.{wk}.verify",
    ]
    return publish, [*subscribe, "_INBOX.>"]


def _nats_server_bin() -> str:
    found = shutil.which("nats-server")
    gobin = Path(os.environ.get("GOPATH", Path.home() / "go")) / "bin" / "nats-server"
    if found:
        return found
    if gobin.exists():
        return str(gobin)
    if os.environ.get("CI"):
        pytest.fail("nats-server not installed; run `make tools`")
    pytest.skip("nats-server not installed; run `make tools`")


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])


@dataclass
class Env:
    url: str
    mode: str
    worker_auth: dict[str, Any]
    account_kp: nkeys.KeyPair | None = None
    callouts: list[dict[str, Any]] = field(default_factory=list)


def _account_kp() -> nkeys.KeyPair:
    return nkeys.from_seed(nkeys.encode_seed(os.urandom(32), nkeys.PREFIX_BYTE_ACCOUNT))


@pytest.fixture(params=["static", "callout"])
def env(request: pytest.FixtureRequest, tmp_path: Path) -> Iterator[Env]:
    publish, subscribe = standard_template(PROVIDER, C.WORKER_NAME)
    port = _free_port()
    conf: dict[str, Any] = {"host": "127.0.0.1", "port": port, "jetstream": {"store_dir": str(tmp_path / "js")}}
    if request.param == "static":
        perms = {"publish": {"allow": publish}, "subscribe": {"allow": subscribe}}
        users = [{"user": "admin", "password": "admin"}, {"user": "worker", "password": "worker", "permissions": perms}]
        conf["authorization"] = {"users": users}
        e = Env("", "static", {"nats_user": "worker", "nats_password": "worker"})
    else:
        # Like core's docker/nats-auth-callout.conf, minus the placeholder nkey user.
        kp = _account_kp()
        conf["accounts"] = {"CAIRN": {"jetstream": "enabled", "users": [{"user": "admin", "password": "admin"}]}}
        conf["authorization"] = {
            "auth_callout": {"issuer": kp.public_key.decode(), "account": "CAIRN", "auth_users": ["admin"]}
        }
        e = Env("", "callout", {"enrollment_token": TOKEN}, kp)
    path = tmp_path / "nats.conf"
    path.write_text(json.dumps(conf))
    proc = subprocess.Popen([_nats_server_bin(), "-c", str(path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)  # noqa: S603
    deadline = time.monotonic() + 10
    while True:
        try:
            socket.create_connection(("127.0.0.1", port), timeout=0.2).close()
            break
        except OSError:
            if time.monotonic() > deadline or proc.poll() is not None:
                proc.kill()
                pytest.fail("nats-server did not start")
            time.sleep(0.05)
    e.url = f"nats://127.0.0.1:{port}"
    yield e
    proc.terminate()
    proc.wait(timeout=10)


def _b64(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()


def _jwt(claims: dict[str, Any], kp: nkeys.KeyPair) -> str:
    """Encode + sign NATS JWT claims the way nats-io/jwt v2 does (ed25519-nkey)."""
    claims = {**claims, "iat": int(time.time()), "iss": kp.public_key.decode(), "jti": ""}
    claims["jti"] = base64.b32encode(hashlib.sha256(json.dumps(claims).encode()).digest()).rstrip(b"=").decode()
    head = _b64(json.dumps({"typ": "JWT", "alg": "ed25519-nkey"}).encode()) + "." + _b64(json.dumps(claims).encode())
    return head + "." + _b64(kp.sign(head.encode()))


def _decode(token: str) -> dict[str, Any]:
    body = token.split(".")[1]
    return cast(dict[str, Any], json.loads(base64.urlsafe_b64decode(body + "=" * (-len(body) % 4))))


async def _serve_callout(nc: NATS, e: Env) -> None:
    """Stand-in for core's AuthCalloutSubscriber: admit TOKEN as the garmin enrollment."""
    kp = e.account_kp
    assert kp is not None
    publish, subscribe = standard_template(PROVIDER, C.WORKER_NAME)

    async def on_auth(m: Msg) -> None:
        req = _decode(m.data.decode())["nats"]
        user_nkey, server_id, opts = req["user_nkey"], req["server_id"]["id"], req["connect_opts"]
        e.callouts.append(opts)
        resp: dict[str, Any] = {"sub": user_nkey, "aud": server_id}
        nats_claims: dict[str, Any] = {"type": "authorization_response", "version": 2}
        nats_claims["issuer_account"] = kp.public_key.decode()
        if opts.get("auth_token") != TOKEN:
            nats_claims["error"] = "unknown_token"
        elif opts.get("name") != C.WORKER_NAME:
            nats_claims["error"] = "name_mismatch"
        else:
            user = {
                "sub": user_nkey,
                "aud": "CAIRN",
                "name": WORKER_KEY,
                "exp": int(time.time()) + 3600,
                "nats": {
                    "pub": {"allow": publish},
                    "sub": {"allow": subscribe},
                    "subs": -1,
                    "data": -1,
                    "payload": -1,
                    "type": "user",
                    "version": 2,
                },
            }
            nats_claims["jwt"] = _jwt(user, kp)
        await m.respond(_jwt({**resp, "nats": nats_claims}, kp).encode())

    await nc.subscribe("$SYS.REQ.USER.AUTH", cb=on_auth)
    await nc.flush()


class BlobStore(BaseHTTPRequestHandler):
    """Stands in for S3 behind the presigned URLs."""

    blobs: ClassVar[dict[str, bytes]] = {}

    def do_PUT(self) -> None:
        self.blobs[self.path] = self.rfile.read(int(self.headers["Content-Length"]))
        self.send_response(200)
        self.end_headers()

    def do_GET(self) -> None:
        body = self.blobs.get(self.path)
        self.send_response(200 if body is not None else 404)
        self.end_headers()
        self.wfile.write(body or b"")

    def log_message(self, *_: Any) -> None:
        pass


@pytest.fixture
def blob_url() -> Iterator[str]:
    srv = ThreadingHTTPServer(("127.0.0.1", 0), BlobStore)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{srv.server_address[1]}"
    srv.shutdown()


class RecentClient:
    """Garmin API stand-in with one activity inside the reconcile window."""

    def __init__(self) -> None:
        self.start_ms = int(datetime.now(UTC).timestamp() * 1000) - 3_600_000

    def list_activities(self, start: int, limit: int) -> list[dict[str, Any]]:
        return [] if start else [{"activityId": 7, "beginTimestamp": self.start_ms}]

    def get_activity(self, ext_id: str) -> dict[str, Any]:
        return {"activityId": ext_id, "beginTimestamp": self.start_ms, "activityType": {"typeKey": "running"}}

    def get_activity_details(self, ext_id: str) -> dict[str, Any]:
        return {
            "metricDescriptors": [{"key": "directTimestamp", "metricsIndex": 0}],
            "activityDetailMetrics": [{"metrics": [self.start_ms]}],
        }

    def daily_health(self, day: str) -> dict[str, float]:
        return {"Steps": 100.0}


async def _until(cond: Callable[[], Awaitable[bool]], what: str) -> None:
    try:
        async with asyncio.timeout(15):
            while True:
                if await cond():
                    return
                await asyncio.sleep(0.05)
    except TimeoutError:
        raise AssertionError(f"timed out waiting for {what}") from None


async def _admin(e: Env, blob_url: str) -> tuple[NATS, list[str], list[bytes]]:
    """Bootstrap streams/KV like core and serve the server-side request/reply subjects."""
    nc = await nats.connect(e.url, user="admin", password="admin")
    if e.mode == "callout":
        await _serve_callout(nc, e)
    js = nc.jetstream()
    await js.add_stream(StreamConfig(name=JOB_STREAM, subjects=["cairn.jobs.>"], retention=RetentionPolicy.WORK_QUEUE))
    await js.add_stream(StreamConfig(name="CAIRN_RESULTS", subjects=["cairn.results.>"]))
    await js.create_key_value(bucket="cairn_worker_presence")
    results: list[str] = []
    bodies: list[bytes] = []
    n = 0

    async def on_result(m: Msg) -> None:
        results.append(m.subject)
        bodies.append(m.data)

    async def presign(m: Msg) -> None:
        nonlocal n
        n += 1
        req = json.loads(m.data)
        # Archives are named by source, so a test can address one whatever the upload order.
        name = f"archive-{req['source_id']}" if req.get("kind") != "result" else f"b{n}"
        await m.respond(json.dumps({"url": f"{blob_url}/{name}", "blob_id": name}).encode())

    async def presign_download(m: Msg) -> None:
        await m.respond(json.dumps({"url": f"{blob_url}/{json.loads(m.data)['blob_id']}"}).encode())

    async def creds(m: Msg) -> None:
        await m.respond(json.dumps({"email": "e@x", "password": "pw"}).encode())

    await nc.subscribe("cairn.results.>", cb=on_result)
    await nc.subscribe(f"cairn.blobs.presign_upload.{PROVIDER}", cb=presign)
    await nc.subscribe(f"cairn.blobs.presign_download.{PROVIDER}", cb=presign_download)
    await nc.subscribe(f"cairn.creds.{PROVIDER}.get", cb=creds)
    await nc.flush()
    return nc, results, bodies


def _violations(caplog: pytest.LogCaptureFixture) -> list[str]:
    return [r.getMessage() + str(r.exc_info) for r in caplog.records if "ermission" in str(r.exc_info) + r.getMessage()]


def test_worker_runs_under_standard_template(env: Env, blob_url: str, caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.DEBUG)

    async def scenario() -> None:
        admin, results, _ = await _admin(env, blob_url)
        ajs = admin.jetstream()
        wk = runtime.Worker(C.Config(nats_url=env.url, garth_home="/nonexistent", **env.worker_auth))
        wk.MAX_DELIVERIES = 1
        wk._clients = {ACCOUNT: cast(GarminClient, RecentClient())}
        run = asyncio.create_task(wk.run())

        async def consumers_ready() -> bool:
            names = {c.name for c in await ajs.consumers_info(JOB_STREAM)}
            pools = {f"{C.WORKER_NAME}-{s}" for s in ("fetch", "metrics", "parseblob", "reconcile")}
            legacy = {f"garmin-{s}" for s in ("fetch", "metrics", "parseblob", "reconcile")}
            return names >= pools | legacy

        await _until(consumers_ready, "durable consumers")
        presence = await ajs.key_value("cairn_worker_presence")

        async def heartbeat() -> bool:
            try:
                await presence.get(f"{C.WORKER_NAME}.{wk.cfg.instance_id}")
            except Exception:  # noqa: BLE001
                return False
            return True

        await _until(heartbeat, "presence heartbeat")

        reply = await admin.request(C.DISCOVER_SUBJECT, json.dumps({"account_id": ACCOUNT}).encode(), 5)
        assert json.loads(reply.data)["items"][0]["external_id"] == "7"
        assert await wk._fetch_creds(ACCOUNT) == ("e@x", "pw")

        job = {"job_id": "j1", "account_id": ACCOUNT, "user_id": "u1", "provider": PROVIDER}
        # reconcile enqueues fetch_source for activity 7, whose result is claim-checked.
        await ajs.publish(C.SUBJ_RECONCILE, json.dumps(job).encode())
        now = int(time.time())
        await ajs.publish(C.SUBJ_METRICS, json.dumps({**job, "since_unix": now, "until_unix": now}).encode())
        await ajs.publish(C.SUBJ_FETCH, json.dumps(job).encode())  # no ext_id → term

        async def all_results() -> bool:
            return {
                f"cairn.results.reconcile.{PROVIDER}.{ACCOUNT}",
                f"cairn.results.fetch_source.{PROVIDER}",
                f"cairn.results.import_metrics.{PROVIDER}",
            } <= set(results)

        await _until(all_results, "results")

        # parse_blob re-presigns the archived blob from its handle.
        blob = {"url": "", "fallback_handle": "archive-7"}
        await ajs.publish(C.SUBJ_PARSE_BLOB, json.dumps({**job, "ext_id": "7", "blob": blob}).encode())

        async def reparsed() -> bool:
            return results.count(f"cairn.results.fetch_source.{PROVIDER}") >= 2

        await _until(reparsed, "parse_blob result")

        # A job queued on the pre-0.5 subject is still drained.
        metrics = {**job, "since_unix": now, "until_unix": now}
        await ajs.publish(C.legacy_subject("import_metrics"), json.dumps(metrics).encode())

        async def legacy_drained() -> bool:
            return results.count(f"cairn.results.import_metrics.{PROVIDER}") >= 2

        await _until(legacy_drained, "legacy subject result")

        async def drained() -> bool:
            return (await ajs.stream_info(JOB_STREAM)).state.messages == 0

        await _until(drained, "acked jobs")
        wk.stop()
        await asyncio.wait_for(run, 15)
        await admin.close()

    asyncio.run(scenario())
    assert _violations(caplog) == []


def test_template_rejects_foreign_subjects(env: Env, blob_url: str, caplog: pytest.LogCaptureFixture) -> None:
    """Control: the server really enforces the template."""

    async def scenario() -> None:
        admin, _, _ = await _admin(env, blob_url)
        wk = runtime.Worker(C.Config(nats_url=env.url, **env.worker_auth))
        await wk.connect()
        await wk._nats.publish(f"cairn.jobs.reconcile.{PROVIDER}", b"{}")
        await wk._nats.publish("cairn.creds.strava.get", b"{}")
        await wk._nats.flush()
        await asyncio.sleep(0.3)
        await wk._nats.close()
        await admin.close()

    asyncio.run(scenario())
    assert len(_violations(caplog)) == 2
    if env.mode == "callout":
        assert len(env.callouts) == 1
        assert "nkey" not in env.callouts[0]  # token only, no client nkey


@pytest.mark.parametrize("env", ["callout"], indirect=True)
def test_token_wins_over_user_password(env: Env, blob_url: str, caplog: pytest.LogCaptureFixture) -> None:
    async def scenario() -> None:
        admin, _, _ = await _admin(env, blob_url)
        cfg = C.Config(nats_url=env.url, enrollment_token=TOKEN, nats_user="admin", nats_password="admin")
        wk = runtime.Worker(cfg)
        await wk.connect()
        await wk._nats.close()
        await admin.close()

    asyncio.run(scenario())
    assert len(env.callouts) == 1
    assert env.callouts[0].get("user") is None
    assert any("ignoring CAIRN_NATS_USER" in r.getMessage() for r in caplog.records)


@pytest.mark.parametrize("env", ["callout"], indirect=True)
def test_callout_refuses_unknown_token(env: Env, blob_url: str) -> None:
    async def scenario() -> None:
        admin, _, _ = await _admin(env, blob_url)
        with pytest.raises(nats.errors.Error):
            await nats.connect(
                env.url, token=BAD_TOKEN, name=C.WORKER_NAME, max_reconnect_attempts=0, allow_reconnect=False
            )
        await admin.close()

    asyncio.run(scenario())
    assert env.callouts[0]["auth_token"] == BAD_TOKEN
