"""NATS runtime: connect, heartbeat, serve discover, pull fetch jobs, publish results.

Job wire (server→worker) is hand-rolled JSON; results are protojson JobResult.
Per-user Garmin credentials are fetched fresh per account via the
cairn.creds.garmin.get request/reply (never queued in a job).
"""

from __future__ import annotations

import asyncio
import contextlib
import json
import logging
from collections.abc import Awaitable, Callable
from datetime import UTC, datetime, timedelta
from typing import Any

import nats
from google.protobuf import json_format
from nats.aio.client import Client as NATS
from nats.aio.msg import Msg
from nats.errors import TimeoutError as NatsTimeout
from nats.js import JetStreamContext

import cairn_garmin  # noqa: F401 (proto path bootstrap)
from cairn.worker.v1 import worker_service_pb2 as w

from . import archive, mapping
from . import config as C
from .garmin_client import GarminClient
from .manifest import manifest

log = logging.getLogger("cairn.garmin")

DISCOVER_SUBJECT = C.DISCOVER_SUBJECT
CREDS_SUBJECT = "cairn.creds.garmin.get"
PER_PAGE = 50

Handler = Callable[[bytes], Awaitable[None]]


class Worker:
    def __init__(self, cfg: C.Config) -> None:
        self.cfg = cfg
        self.nc: NATS | None = None
        self.js: JetStreamContext | None = None
        self._stop = asyncio.Event()
        self._clients: dict[str, GarminClient] = {}  # account_id → client
        self._reconciled_at: dict[str, float] = {}  # account_id → loop time of last real reconcile
        self._fatal: Exception | None = None  # set when core moves to an incompatible release

    @property
    def _nats(self) -> NATS:
        if self.nc is None:
            raise RuntimeError("not connected to NATS")
        return self.nc

    @property
    def _js(self) -> JetStreamContext:
        if self.js is None:
            raise RuntimeError("not connected to JetStream")
        return self.js

    @property
    def worker_key(self) -> str:
        return f"{C.WORKER_NAME}-{C.PROVIDER}"

    async def connect(self) -> None:
        # The auth-callout matches the connection name against the enrollment name.
        opts: dict[str, Any] = {"name": C.WORKER_NAME, "max_reconnect_attempts": -1}
        if self.cfg.enrollment_token:
            if self.cfg.nats_user:
                log.warning("CAIRN_WORKER_ENROLLMENT_TOKEN is set; ignoring CAIRN_NATS_USER/CAIRN_NATS_PASSWORD")
            opts["token"] = self.cfg.enrollment_token
        elif self.cfg.nats_user:
            opts["user"] = self.cfg.nats_user
            opts["password"] = self.cfg.nats_password
        nc = await nats.connect(self.cfg.nats_url, **opts)
        self.nc, self.js = nc, nc.jetstream()
        log.info("connected to %s", self.cfg.nats_url)

    async def run(self) -> None:
        await self.connect()
        await self._check_core_release()
        await self._nats.subscribe(DISCOVER_SUBJECT, cb=self._on_discover)
        jobs: list[tuple[str, str, Handler]] = [
            ("fetch_source", "fetch", self._handle_fetch_source),
            ("import_metrics", "metrics", self._handle_import_metrics),
            ("parse_blob", "parseblob", self._handle_parse_blob),
            ("reconcile", "reconcile", self._handle_reconcile),
            ("import_gear", "gear", self._handle_import_gear),
        ]
        tasks = [asyncio.create_task(self._heartbeat_loop())]
        for job, suffix, handler in jobs:
            tasks.append(asyncio.create_task(self._consume(C.job_subject(job), f"{C.WORKER_NAME}-{suffix}", handler)))
            # Pre-0.5 subject with its old durable, drained once. Remove in 0.6.
            tasks.append(asyncio.create_task(self._drain_legacy(C.legacy_subject(job), f"garmin-{suffix}", handler)))
        log.info(
            "serving %s; pulling %s, %s, %s, %s, %s",
            DISCOVER_SUBJECT,
            C.SUBJ_FETCH,
            C.SUBJ_METRICS,
            C.SUBJ_PARSE_BLOB,
            C.SUBJ_RECONCILE,
            C.SUBJ_GEAR,
        )
        await self._stop.wait()
        for t in tasks:
            t.cancel()
        if self.nc:
            await self.nc.drain()
        if self._fatal is not None:
            raise self._fatal

    async def _check_core_release(self) -> None:
        """Refuse to run against a core of another major.minor (core ADR 0005)."""
        try:
            kv = await self._js.key_value(C.CORE_INFO_KV)
            entry = await kv.get("info")
            core = json.loads(entry.value or b"{}").get("release", "")
        except Exception as e:  # noqa: BLE001 — older core or not yet published
            log.debug("core info unavailable: %s", e)
            return
        if not release_compatible(core, C.RELEASE):
            raise IncompatibleCoreError(f"core {core}, worker {C.RELEASE}: major.minor must match")

    def stop(self) -> None:
        self._stop.set()

    # --- credentials + client cache ---
    async def _client_for(self, account_id: str) -> GarminClient:
        if account_id in self._clients:
            return self._clients[account_id]
        email, password = await self._fetch_creds(account_id)
        garth_home = f"{self.cfg.garth_home}/{account_id or 'default'}"
        client = GarminClient(email, password, garth_home)
        self._clients[account_id] = client
        return client

    async def _fetch_creds(self, account_id: str) -> tuple[str, str]:
        if account_id and self.nc is not None:
            try:
                resp = await self.nc.request(CREDS_SUBJECT, json.dumps({"account_id": account_id}).encode(), timeout=5)
                data = json.loads(resp.data)
                if not data.get("error") and data.get("email"):
                    return data["email"], data.get("password", "")
                log.warning("creds rpc for %s: %s", account_id, data.get("error"))
            except Exception as e:  # noqa: BLE001
                log.warning("creds rpc failed for %s: %s", account_id, e)
        if self.cfg.garmin_email and self.cfg.garmin_password:
            return self.cfg.garmin_email, self.cfg.garmin_password
        raise RuntimeError(f"no Garmin credentials for account {account_id}")

    # --- heartbeat ---
    async def _heartbeat_loop(self) -> None:
        kv = await self._js.key_value(C.PRESENCE_KV)  # created by the server's stream bootstrap
        key = f"{C.WORKER_NAME}.{self.cfg.instance_id}"
        while not self._stop.is_set():
            payload = {
                "worker_name": C.WORKER_NAME,
                "worker_key": self.worker_key,
                "instance_id": self.cfg.instance_id,
                "version": C.VERSION,
                "release": C.RELEASE,
                "provider": C.PROVIDER,
                "package": C.PACKAGE,
                "webhooks": False,
                "capabilities": manifest(),
                "last_seen": datetime.now(UTC).isoformat(),
            }
            try:
                await kv.put(key, json.dumps(payload).encode())
            except Exception as e:  # noqa: BLE001
                log.debug("heartbeat failed: %s", e)
            # Core upgraded underneath us: stop instead of mis-parsing.
            try:
                await self._check_core_release()
            except IncompatibleCoreError as e:
                self._fatal = e
                self._stop.set()
                return
            with contextlib.suppress(TimeoutError):
                await asyncio.wait_for(self._stop.wait(), timeout=self.cfg.heartbeat_interval_s)

    # --- discover (request/reply): list activities for a page ---
    async def _on_discover(self, msg: Msg) -> None:
        try:
            req = json.loads(msg.data)
            account_id = req.get("account_id", "")
            page = max(int(req.get("start_page", 1) or 1), 1)
            client = await self._client_for(account_id)
            offset = (page - 1) * PER_PAGE
            acts = await asyncio.to_thread(client.list_activities, offset, PER_PAGE)
            if not acts:
                resp = {"items": [], "complete": True}
            else:
                items = [
                    {
                        "item_type": "activity",
                        "external_id": str(a.get("activityId")),
                        "item_time": _activity_time(a),
                    }
                    for a in acts
                    if a.get("activityId") is not None
                ]
                resp = {"items": items, "next_page": page + 1}
        except Exception as e:  # noqa: BLE001
            log.error("discover error: %s", e)
            resp = {"error": str(e)}
        await msg.respond(json.dumps(resp).encode())

    # --- fetch_source (pull): import one activity ---

    # A job that keeps failing (activity gone upstream, unmappable payload)
    # is terminated after this many deliveries instead of NAK-looping forever.
    # The server's stale-queue reaper then fails the import-queue item.
    MAX_DELIVERIES = 5
    # Re-parse jobs handed back as parser_too_old: give a newer instance about
    # 35 minutes to join the pool before telling core.
    PARSER_TOO_OLD_ATTEMPTS = 10
    # How long a failed job waits before redelivery — keeps a failing
    # activity from hot-looping against the Garmin API.
    NAK_DELAY_S = 60
    # Ack-deadline extension cadence; must stay below the consumer AckWait
    # (default 30s). Covers slow handlers AND messages waiting in the batch.
    ACK_EXTEND_S = 10

    async def _extend_ack(self, m: Msg) -> None:
        # Ends on cancel, or once the message is acked/naked or the delivery is gone.
        with contextlib.suppress(asyncio.CancelledError, Exception):
            while True:
                await asyncio.sleep(self.ACK_EXTEND_S)
                await m.in_progress()

    async def _drain_legacy(self, subject: str, durable: str, handler: Handler) -> None:
        try:
            await self._consume(subject, durable, handler)
        except Exception as e:  # noqa: BLE001 — another pool may hold it (work queues allow one)
            log.warning("legacy subject %s not drained: %s", subject, e)

    async def _consume(self, subject: str, durable: str, handler: Handler) -> None:
        psub = await self._js.pull_subscribe(subject, durable=durable, stream=C.JOB_STREAM)
        while not self._stop.is_set():
            try:
                msgs = await psub.fetch(self.cfg.pull_batch, timeout=5)
            except NatsTimeout:
                continue
            except Exception as e:  # noqa: BLE001
                log.warning("fetch error on %s: %s", subject, e)
                await asyncio.sleep(1)
                continue
            # Extend every fetched message's ack deadline from arrival: the
            # batch is processed sequentially, and without this a slow handler
            # pushes the waiting messages past AckWait into redelivery loops.
            heartbeats = [asyncio.create_task(self._extend_ack(m)) for m in msgs]
            for m, hb in zip(msgs, heartbeats, strict=True):
                try:
                    await handler(m.data)
                    await m.ack()
                except TerminalJobError as e:
                    log.error("handler error on %s (terminal): %s", subject, e)
                    await self._publish_failure(subject, m.data, e)
                    await m.term()
                except ParserTooOldError as e:
                    # Rolling upgrade: a newer instance of the pool takes it. Does
                    # not count as a failure until the back-off window is over.
                    deliveries = m.metadata.num_delivered or 1
                    if deliveries >= self.PARSER_TOO_OLD_ATTEMPTS:
                        log.error("handler error on %s (parser too old, giving up): %s", subject, e)
                        await self._publish_failure(subject, m.data, e)
                        await m.term()
                    else:
                        await m.nak(delay=min(30 * 2 ** (deliveries - 1), 600))
                except Exception as e:  # noqa: BLE001
                    deliveries = m.metadata.num_delivered or 1
                    if deliveries >= self.MAX_DELIVERIES:
                        log.error("handler error on %s (delivery %d, terminating): %s", subject, deliveries, e)
                        await self._publish_failure(subject, m.data, e)
                        await m.term()
                    else:
                        log.error(
                            "handler error on %s (delivery %d/%d): %s", subject, deliveries, self.MAX_DELIVERIES, e
                        )
                        await m.nak(delay=self.NAK_DELAY_S)
                finally:
                    hb.cancel()

    async def _publish_result(self, subject: str, jr: w.JobResult) -> None:
        """Publish a JobResult. Event-carrying results are claim-checked:
        the full protojson body goes to the blob store and only a small
        envelope with payload_ref travels over NATS, so stream-heavy
        activities can't exceed the broker's max_payload. Event-free
        results (nothing to spill) publish inline.
        """
        body = json_format.MessageToJson(jr).encode()
        if not jr.events:
            await self._js.publish(subject, body)
            return
        ref = await archive.upload_result(self._nats, body)
        env = w.JobResult(
            worker_name=jr.worker_name,
            worker_version=jr.worker_version,
            worker_package=jr.worker_package,
            worker_release=jr.worker_release,
            more_available=jr.more_available,
        )
        if jr.HasField("new_watermark"):
            env.new_watermark.CopyFrom(jr.new_watermark)
        env.payload_ref.blob_id = ref["blob_id"]
        env.payload_ref.size_bytes = ref["size"]
        env.payload_ref.content_type = "application/json"
        env.payload_ref.content_sha256 = ref["sha256"]
        await self._js.publish(subject, json_format.MessageToJson(env).encode())

    async def _publish_failure(self, job_subject: str, body: bytes, err: Exception) -> None:
        """Best-effort failure envelope published alongside a Term, so the
        server fails the import-queue item with the true reason instead of
        the stale reaper's masked "no result after N dispatch attempts".
        """
        try:
            job = json.loads(body)
        except Exception:  # noqa: BLE001
            return
        ext_id = str(job.get("ext_id") or "")
        if not ext_id:
            return
        jr = w.JobResult(
            worker_name=C.WORKER_NAME, worker_version=C.VERSION, worker_package=C.PACKAGE, worker_release=C.RELEASE
        )
        setattr(jr.error, "class", w.ERROR_CLASS_WORKER_BUG)
        jr.error.code = getattr(err, "code", type(err).__name__)
        jr.error.message = str(err)[:500]
        jr.failed_ref.user_id = str(job.get("user_id") or "")
        jr.failed_ref.provider = C.PROVIDER
        jr.failed_ref.external_account_id = str(job.get("account_id") or "")
        jr.failed_ref.external_id = ext_id
        subject = result_subject(job_subject)
        try:
            await self._js.publish(subject, json_format.MessageToJson(jr).encode())
        except Exception as e:  # noqa: BLE001
            log.warning("failure result publish failed for %s: %s", ext_id, e)

    async def _handle_fetch_source(self, body: bytes) -> None:
        job = json.loads(body)
        ext_id = job.get("ext_id")
        if not ext_id:
            raise ValueError("missing ext_id")
        account_id = job.get("account_id", "")
        user_id = job.get("user_id", "")
        client = await self._client_for(account_id)
        act = await asyncio.to_thread(client.get_activity, ext_id)

        details = None
        if job.get("fetch_streams"):
            details = await asyncio.to_thread(client.get_activity_details, ext_id)
        # Gear is optional data: one extra call, never fails the import.
        gear = await self._activity_gear(client, str(ext_id))

        # The archive holds every parser input, so a re-parse reproduces this
        # import (core ADR 0005). Archiving is best-effort.
        env = archive.envelope(act, details, gear)
        blob_id, blob_size = await archive.archive(self._nats, user_id, str(ext_id), env)
        events = mapping.parse_archive(
            env, user_id=user_id, account_id=account_id, ext_id=str(ext_id), blob_id=blob_id or ""
        )
        if blob_id:
            imported = events[-1].activity
            imported.raw_content_type = "application/json"
            imported.raw_size_bytes = blob_size

        await self._publish_result(C.RESULT_SUBJECT, self._job_result(events))
        log.info("published activity %s for user %s", ext_id, job.get("user_id"))

    async def _activity_gear(self, client: GarminClient, ext_id: str) -> list[dict[str, Any]] | None:
        """None when not looked up (disabled or failed), so the archive says so."""
        if not self.cfg.fetch_activity_gear:
            return None
        try:
            return await asyncio.to_thread(client.activity_gear, ext_id)
        except Exception as e:  # noqa: BLE001 — gear is optional
            log.warning("activity gear lookup failed for %s: %s", ext_id, e)
            return None

    def _job_result(self, events: list[w.WorkerEvent]) -> w.JobResult:
        return mapping.job_result(events, name=C.WORKER_NAME, version=C.VERSION, package=C.PACKAGE, release=C.RELEASE)

    async def _handle_import_gear(self, body: bytes) -> None:
        job = json.loads(body)
        account_id = job.get("account_id", "")
        user_id = job.get("user_id", "")
        client = await self._client_for(account_id)
        gear = await asyncio.to_thread(client.gear)
        try:
            defaults = mapping.gear_default_types(await asyncio.to_thread(client.gear_defaults))
        except Exception as e:  # noqa: BLE001 — defaults are a nicety
            log.warning("gear defaults lookup failed: %s", e)
            defaults = {}
        events = [
            mapping.gear_event(user_id, account_id, rec, defaults.get(str(rec.get("uuid")), []))
            for rec in gear
            if rec.get("uuid")
        ]
        if not events:
            log.info("no gear on account %s", account_id)
            return
        await self._publish_result(C.RESULT_GEAR, self._job_result(events))
        log.info("published %d gear for user %s", len(events), user_id)

    async def _handle_parse_blob(self, body: bytes) -> None:
        """Re-parse an archived activity with current mapping logic — no Garmin
        API call. Downloads the stored envelope, re-maps it, and republishes;
        the server's ingest finds the existing source and replaces the payload.
        """
        job = json.loads(body)
        # Rolling upgrade: leave it to a newer instance of the pool.
        min_parser = job.get("min_parser_version", "")
        if not parser_allows(C.VERSION, min_parser):
            raise ParserTooOldError(f"source parsed by {min_parser}, this parser is {C.VERSION}")
        blob = job.get("blob") or {}
        ext_id = job.get("ext_id", "")
        fallback = blob.get("fallback_handle", "")

        env = await archive.fetch(self._nats, blob.get("url", ""), fallback)
        if env.get("version") != C.DATASET_VERSION:
            raise TerminalJobError(f"archive dataset {env.get('version')}, parser reads {C.DATASET_VERSION}")
        events = mapping.parse_archive(
            env,
            user_id=job.get("user_id", ""),
            account_id=job.get("account_id", ""),
            ext_id=str(ext_id),
            blob_id=fallback,
        )
        await self._publish_result(C.RESULT_SUBJECT, self._job_result(events))
        log.info("re-parsed activity %s for user %s", ext_id, job.get("user_id"))

    # --- reconcile (pull): catch new activity since the watermark ---

    # Reconcile never lists further back than this, even without a watermark —
    # full-history backfill is the user-driven import queue's job.
    RECONCILE_LOOKBACK_DAYS = 30
    # Cap on fetch_source sub-jobs one reconcile run enqueues.
    RECONCILE_MAX_ENQUEUE = 500
    # Coalescing window: reconcile jobs for an account handled more recently
    # than this are acked without touching the Garmin API. Drains a scheduler
    # backlog (jobs queued while no reconcile consumer existed) as no-ops.
    RECONCILE_COALESCE_S = 600

    async def _handle_reconcile(self, body: bytes) -> None:
        job = json.loads(body)
        account_id = job.get("account_id", "")
        job_id = job.get("job_id", "")

        now = asyncio.get_running_loop().time()
        last = self._reconciled_at.get(account_id)
        if last is not None and now - last < self.RECONCILE_COALESCE_S:
            return  # coalesced — ack without API calls
        self._reconciled_at[account_id] = now

        watermark = _parse_watermark(job.get("watermark"))
        # Window start: the later of (watermark - 1h drift margin) and the
        # lookback floor — always bounded to recent activity, never a flood.
        window_start = datetime.now(UTC) - timedelta(days=self.RECONCILE_LOOKBACK_DAYS)
        if watermark is not None:
            window_start = max(window_start, watermark - timedelta(hours=1))

        enqueued, high_water = await self._enqueue_unseen(job, window_start)
        if watermark is not None:
            high_water = max(high_water or watermark, watermark)

        # The result MUST be published even when nothing new was found —
        # advancing last_sync_at is what stops the scheduler from re-polling
        # the account every tick. Account-suffixed subject for attribution.
        jr = self._job_result([])
        if high_water is not None:
            jr.new_watermark.FromDatetime(high_water)
        await self._js.publish(
            f"{C.RESULT_RECONCILE_PREFIX}.{account_id}",
            json_format.MessageToJson(jr).encode(),
            headers={"Nats-Msg-Id": f"result:{job_id}"},
        )
        log.info("reconcile for %s: %d new activity job(s) enqueued", account_id, enqueued)

    async def _enqueue_unseen(self, job: dict[str, Any], window_start: datetime) -> tuple[int, datetime | None]:
        """Enqueue fetch_source for listed activities inside the window and not yet known.
        Returns the number enqueued and the newest enqueued start time."""
        max_enqueue = int(job.get("max_enqueue") or 0) or self.RECONCILE_MAX_ENQUEUE
        known = set(job.get("known_ext_ids") or [])
        client = await self._client_for(job.get("account_id", ""))
        enqueued = 0
        high_water: datetime | None = None
        offset, page_size = 0, PER_PAGE
        while enqueued < max_enqueue:
            acts = await asyncio.to_thread(client.list_activities, offset, page_size)
            if not acts:
                break
            page_fully_in_window = True
            for a in acts:
                if a.get("activityId") is None:
                    continue
                ext_id = str(a["activityId"])
                ms = mapping.start_ms(a)
                start = datetime.fromtimestamp(ms / 1000, tz=UTC) if ms else None
                if start is not None and start < window_start:
                    page_fully_in_window = False
                    continue  # newest-first listing: rest of page is older
                if ext_id in known:
                    continue
                await self._enqueue_fetch(job, ext_id)
                enqueued += 1
                if start is not None:
                    high_water = max(high_water or start, start)
                if enqueued >= max_enqueue:
                    break
            if not page_fully_in_window or len(acts) < page_size:
                break
            offset += page_size
        return enqueued, high_water

    async def _enqueue_fetch(self, job: dict[str, Any], ext_id: str) -> None:
        account_id = job.get("account_id", "")
        fetch_body = json.dumps(
            {
                "job_id": f"{job.get('job_id', '')}:{ext_id}",
                "account_id": account_id,
                "user_id": job.get("user_id", ""),
                "provider": C.PROVIDER,
                "ext_id": ext_id,
                "fetch_streams": True,
                "reason": "reconcile",
            }
        ).encode()
        # Deterministic msg-id: duplicate enqueues within JetStream's
        # dedup window collapse; ingest dedups idempotently beyond it.
        msg_id = f"reconcile:{C.PROVIDER}:{account_id}:{ext_id}"
        await self._js.publish(C.SUBJ_FETCH, fetch_body, headers={"Nats-Msg-Id": msg_id})

    async def _handle_import_metrics(self, body: bytes) -> None:
        job = json.loads(body)
        account_id = job.get("account_id", "")
        user_id = job.get("user_id", "")
        client = await self._client_for(account_id)
        since = datetime.fromtimestamp(int(job.get("since_unix", 0)), tz=UTC).date()
        until = datetime.fromtimestamp(int(job.get("until_unix", 0)), tz=UTC).date()

        events: list[w.WorkerEvent] = []
        day = since
        while day <= until and (day - since).days <= 365:
            day_ms = int(datetime(day.year, day.month, day.day, tzinfo=UTC).timestamp() * 1000)
            health = await asyncio.to_thread(client.daily_health, day.isoformat())
            for key, value in health.items():
                events.append(mapping.metric_event(user_id, account_id, key, day_ms, float(value)))
            day += timedelta(days=1)

        if not events:
            return
        await self._publish_result(C.RESULT_METRICS, self._job_result(events))
        log.info("published %d health metrics for user %s", len(events), user_id)


def _parse_watermark(raw: str | None) -> datetime | None:
    if not raw:
        return None
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        log.warning("reconcile: unparseable watermark %r", raw)
        return None


def _activity_time(act: dict[str, Any]) -> str:
    ms = mapping.start_ms(act)
    if ms:
        return datetime.fromtimestamp(ms / 1000, tz=UTC).isoformat()
    return ""


class TerminalJobError(Exception):
    """A job no retry can fix: fail it at once."""


class ParserTooOldError(Exception):
    """The source was parsed by a newer parser; another pool instance takes it."""

    code = "parser_too_old"


class IncompatibleCoreError(RuntimeError):
    """Core runs another release major.minor than this worker."""


def result_subject(job_subject: str) -> str:
    """Results are per pool (core ADR 0006): the pool token stays
    (cairn.jobs.fetch_source.garmin.w1 → cairn.results.fetch_source.garmin.w1).
    """
    if job_subject.startswith("cairn.jobs."):
        return "cairn.results." + job_subject.removeprefix("cairn.jobs.")
    return job_subject + ".result"


def _major_minor(v: str) -> tuple[int, int] | None:
    parts = v.removeprefix("v").split("-", 1)[0].split(".")
    if not v.startswith("v") or len(parts) < 2 or not all(p.isdigit() for p in parts[:2]):
        return None
    return int(parts[0]), int(parts[1])


def release_compatible(core: str, worker: str) -> bool:
    """Core ADR 0005: before 1.0 both share major.minor; from 1.0 on, same major
    and the worker's minor not above core's. Untagged builds are exempt.
    """
    c, wv = _major_minor(core), _major_minor(worker)
    if c is None or wv is None:
        return True
    if c[0] != wv[0]:
        return False
    if c[0] == 0:
        return c[1] == wv[1]
    return wv[1] <= c[1]


def _parser_version(v: str) -> tuple[int, int] | None:
    major, _, minor = v.strip().partition(".")
    if not major.isdigit() or (minor and not minor.isdigit()):
        return None
    return int(major), int(minor or 0)


def parser_allows(own: str, min_version: str) -> bool:
    """Parser own may re-parse a source last parsed by min_version: same
    dataset, own not older (core ADR 0005). Legacy "N" reads as N.0.
    """
    if not min_version:
        return True
    m = _parser_version(min_version)
    if m is None:
        return own == min_version
    o = _parser_version(own)
    return o is not None and o[0] == m[0] and o[1] >= m[1]
