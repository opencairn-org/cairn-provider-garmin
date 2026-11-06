"""The Garmin worker on the Cairn provider SDK: discover, fetch_source,
import_gear, parse_blob, reconcile and import_metrics handlers.

The SDK owns the NATS runtime (connection, presence, manifest, consumers,
claim-checked results, failure envelopes). Per-user Garmin credentials are
fetched fresh per account via cairn.creds.garmin.get (never queued in a job).
"""

from __future__ import annotations

import asyncio
import logging
from datetime import UTC, datetime, timedelta
from typing import Any

from cairn.worker.v1 import worker_service_pb2 as w
from cairn_provider_sdk import CredentialsError, Job, ParserTooOldError, TerminalJobError, parser_allows
from cairn_provider_sdk import Worker as SDKWorker
from cairn_provider_sdk import reconcile as R

from . import config as C
from . import mapping
from .garmin_client import GarminClient
from .manifest import manifest, provider_meta

log = logging.getLogger("cairn.garmin")

DISCOVER_SUBJECT = C.DISCOVER_SUBJECT
CREDS_SUBJECT = C.CREDS_SUBJECT
PER_PAGE = 50


class Worker(SDKWorker):
    # Reconcile never lists further back than this, even without a watermark —
    # full-history backfill is the user-driven import queue's job.
    RECONCILE_LOOKBACK_DAYS = R.LOOKBACK_DAYS
    # Cap on fetch_source sub-jobs one reconcile run enqueues.
    RECONCILE_MAX_ENQUEUE = R.MAX_ENQUEUE
    # Coalescing window: reconcile jobs for an account handled more recently
    # than this are acked without touching the Garmin API. Drains a scheduler
    # backlog (jobs queued while no reconcile consumer existed) as no-ops.
    RECONCILE_COALESCE_S = R.COALESCE_S

    def __init__(self, cfg: C.Config) -> None:
        super().__init__(C.IDENTITY, cfg, manifest=manifest, provider_meta=provider_meta)
        self.cfg: C.Config = cfg
        self._clients: dict[str, GarminClient] = {}  # account_id → client
        self._coalescer = R.Coalescer(self.RECONCILE_COALESCE_S)
        self.handle("fetch_source", self._handle_fetch_source)
        self.handle("import_metrics", self._handle_import_metrics)
        self.handle("parse_blob", self._handle_parse_blob)
        self.handle("reconcile", self._handle_reconcile)
        self.handle("import_gear", self._handle_import_gear)
        self.on_discover(self.discover)

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
                creds = await self.fetch_creds(account_id)
                return creds.client_id, creds.client_secret
            except CredentialsError:
                pass  # logged by the SDK; the env fallback below
        if self.cfg.garmin_email and self.cfg.garmin_password:
            return self.cfg.garmin_email, self.cfg.garmin_password
        raise RuntimeError(f"no Garmin credentials for account {account_id}")

    # --- discover (request/reply): list activities for a page ---
    async def discover(self, req: dict[str, Any]) -> dict[str, Any]:
        account_id = req.get("account_id", "")
        page = max(int(req.get("start_page", 1) or 1), 1)
        client = await self._client_for(account_id)
        offset = (page - 1) * PER_PAGE
        acts = await asyncio.to_thread(client.list_activities, offset, PER_PAGE)
        if not acts:
            return {"items": [], "complete": True}
        items = [
            {"item_type": "activity", "external_id": str(a.get("activityId")), "item_time": _activity_time(a)}
            for a in acts
            if a.get("activityId") is not None
        ]
        return {"items": items, "next_page": page + 1}

    # --- fetch_source (pull): import one activity ---
    async def _handle_fetch_source(self, job: Job) -> None:
        d = job.data
        ext_id = d.get("ext_id")
        if not ext_id:
            raise ValueError("missing ext_id")
        account_id = d.get("account_id", "")
        user_id = d.get("user_id", "")
        client = await self._client_for(account_id)
        act = await asyncio.to_thread(client.get_activity, ext_id)

        details = None
        if d.get("fetch_streams"):
            details = await asyncio.to_thread(client.get_activity_details, ext_id)
        # Gear is optional data: one extra call, never fails the import.
        gear = await self._activity_gear(client, str(ext_id))

        # The archive holds every parser input, so a re-parse reproduces this
        # import (core ADR 0005). Archiving is best-effort.
        env = mapping.envelope(act, details, gear)
        blob_id, blob_size = await self.archive(user_id, str(ext_id), env)
        events = mapping.parse_archive(
            env, user_id=user_id, account_id=account_id, ext_id=str(ext_id), blob_id=blob_id or ""
        )
        if blob_id:
            imported = events[-1].activity
            imported.raw_content_type = "application/json"
            imported.raw_size_bytes = blob_size

        await self.publish_result(C.RESULT_SUBJECT, self.job_result(events))
        log.info("published activity %s for user %s", ext_id, user_id)

    async def _activity_gear(self, client: GarminClient, ext_id: str) -> list[dict[str, Any]] | None:
        """None when not looked up (disabled or failed), so the archive says so."""
        if not self.cfg.fetch_activity_gear:
            return None
        try:
            return await asyncio.to_thread(client.activity_gear, ext_id)
        except Exception as e:  # noqa: BLE001 — gear is optional
            log.warning("activity gear lookup failed for %s: %s", ext_id, e)
            return None

    async def _handle_import_gear(self, job: Job) -> None:
        d = job.data
        account_id = d.get("account_id", "")
        user_id = d.get("user_id", "")
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
        await self.publish_result(C.RESULT_GEAR, self.job_result(events))
        log.info("published %d gear for user %s", len(events), user_id)

    async def _handle_parse_blob(self, job: Job) -> None:
        """Re-parse an archived activity with current mapping logic — no Garmin
        API call. Downloads the stored envelope, re-maps it, and republishes;
        the server's ingest finds the existing source and replaces the payload.
        """
        d = job.data
        # Rolling upgrade: leave it to a newer instance of the pool.
        min_parser = d.get("min_parser_version", "")
        if not parser_allows(C.VERSION, min_parser):
            raise ParserTooOldError(f"source parsed by {min_parser}, this parser is {C.VERSION}")
        blob = d.get("blob") or {}
        ext_id = d.get("ext_id", "")
        fallback = blob.get("fallback_handle", "")

        env = await self.fetch_blob(blob.get("url", ""), fallback)
        if env.get("version") != C.DATASET_VERSION:
            raise TerminalJobError(f"archive dataset {env.get('version')}, parser reads {C.DATASET_VERSION}")
        events = mapping.parse_archive(
            env, user_id=d.get("user_id", ""), account_id=d.get("account_id", ""), ext_id=str(ext_id), blob_id=fallback
        )
        await self.publish_result(C.RESULT_SUBJECT, self.job_result(events))
        log.info("re-parsed activity %s for user %s", ext_id, d.get("user_id"))

    # --- reconcile (pull): catch new activity since the watermark ---
    async def _handle_reconcile(self, job: Job) -> None:
        d = job.data
        account_id = d.get("account_id", "")
        if not self._coalescer.should_run(account_id):
            return  # coalesced — ack without API calls

        watermark = R.parse_watermark(d.get("watermark"))
        window_start = R.window_start(watermark, lookback_days=self.RECONCILE_LOOKBACK_DAYS)
        enqueued, high_water = await self._enqueue_unseen(d, window_start)
        if watermark is not None:
            high_water = max(high_water or watermark, watermark)
        # Published even when nothing new was found (SDK): advancing
        # last_sync_at is what stops the scheduler from re-polling.
        await self.publish_reconcile_result(d, high_water)
        log.info("reconcile for %s: %d new activity job(s) enqueued", account_id, enqueued)

    async def _enqueue_unseen(self, job: dict[str, Any], window_start: datetime) -> tuple[int, datetime | None]:
        """Enqueue fetch_source for listed activities inside the window and not yet known.
        Returns the number enqueued and the newest enqueued start time."""
        max_enqueue = R.max_enqueue(job, self.RECONCILE_MAX_ENQUEUE)
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
                await self.enqueue_fetch(job, ext_id)
                enqueued += 1
                if start is not None:
                    high_water = max(high_water or start, start)
                if enqueued >= max_enqueue:
                    break
            if not page_fully_in_window or len(acts) < page_size:
                break
            offset += page_size
        return enqueued, high_water

    async def _handle_import_metrics(self, job: Job) -> None:
        d = job.data
        account_id = d.get("account_id", "")
        user_id = d.get("user_id", "")
        client = await self._client_for(account_id)
        since = datetime.fromtimestamp(int(d.get("since_unix", 0)), tz=UTC).date()
        until = datetime.fromtimestamp(int(d.get("until_unix", 0)), tz=UTC).date()

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
        await self.publish_result(C.RESULT_METRICS, self.job_result(events))
        log.info("published %d health metrics for user %s", len(events), user_id)


def _activity_time(act: dict[str, Any]) -> str:
    ms = mapping.start_ms(act)
    if ms:
        return datetime.fromtimestamp(ms / 1000, tz=UTC).isoformat()
    return ""
