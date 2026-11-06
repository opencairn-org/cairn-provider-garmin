"""Reconcile handler: lists recent activities, enqueues fetch_source for
unknown ones, always publishes an account-suffixed result with the new
watermark, and coalesces backlog jobs without API calls."""

import asyncio
import json
from datetime import UTC, datetime, timedelta
from typing import Any

from cairn_provider_sdk import Job

from cairn_garmin import config as C
from tests.fakes import job_result, make_worker


class FakeClient:
    def __init__(self, activities: list[dict[str, Any]]) -> None:
        self.activities = activities
        self.list_calls = 0

    def list_activities(self, start: int, limit: int) -> list[dict[str, Any]]:
        self.list_calls += 1
        return self.activities[start : start + limit]


def _act(ext_id: int, start: datetime) -> dict[str, Any]:
    return {"activityId": ext_id, "beginTimestamp": int(start.timestamp() * 1000)}


def _job(**over: Any) -> Job:
    base: dict[str, Any] = {"job_id": "j1", "account_id": "acc-1", "user_id": "u-1", "provider": "garmin"}
    base.update(over)
    return Job.of(base, subject=C.SUBJ_RECONCILE)


def test_reconcile_enqueues_unknown_and_publishes_watermark() -> None:
    now = datetime.now(UTC)
    wm = now - timedelta(days=2)
    client = FakeClient(
        [
            _act(101, now - timedelta(hours=1)),  # new → enqueue
            _act(100, now - timedelta(days=1)),  # new → enqueue
            _act(99, now - timedelta(days=10)),  # older than watermark window → stop
        ]
    )
    wk, js = make_worker(client)

    asyncio.run(wk._handle_reconcile(_job(watermark=wm.isoformat())))

    fetches = [(s, d, h) for s, d, h in js.published if s == C.SUBJ_FETCH]
    assert [json.loads(d)["ext_id"] for _, d, _ in fetches] == ["101", "100"]
    assert fetches[0][2]["Nats-Msg-Id"] == "reconcile:garmin:acc-1:101"
    assert json.loads(fetches[0][1])["reason"] == "reconcile"

    results = [(s, d) for s, d, _ in js.published if s.startswith(C.RESULT_RECONCILE_PREFIX)]
    assert len(results) == 1
    subject, data = results[0]
    assert subject == f"{C.RESULT_RECONCILE_PREFIX}.acc-1"
    jr = job_result(data)
    got = jr.new_watermark.ToDatetime(tzinfo=UTC)
    assert abs((got - (now - timedelta(hours=1))).total_seconds()) < 1


def test_reconcile_empty_still_publishes_result() -> None:
    # Advancing last_sync_at on "nothing new" is what stops the scheduler
    # from re-polling the account every tick.
    wk, js = make_worker(FakeClient([]))
    asyncio.run(wk._handle_reconcile(_job()))

    results = [s for s, _, _ in js.published if s.startswith(C.RESULT_RECONCILE_PREFIX)]
    assert results == [f"{C.RESULT_RECONCILE_PREFIX}.acc-1"]


def test_reconcile_skips_known_ext_ids() -> None:
    now = datetime.now(UTC)
    wk, js = make_worker(FakeClient([_act(101, now - timedelta(hours=1))]))
    asyncio.run(wk._handle_reconcile(_job(known_ext_ids=["101"])))

    fetches = [s for s, _, _ in js.published if s == C.SUBJ_FETCH]
    assert fetches == []


def test_reconcile_coalesces_backlog() -> None:
    now = datetime.now(UTC)
    client = FakeClient([_act(101, now - timedelta(hours=1))])
    wk, js = make_worker(client)

    asyncio.run(wk._handle_reconcile(_job()))
    first_publishes = len(js.published)
    assert client.list_calls == 1

    # Backlog drain: same account again within the coalescing window —
    # no API call, no publish, just an ack.
    asyncio.run(wk._handle_reconcile(_job(job_id="j2")))
    assert client.list_calls == 1
    assert len(js.published) == first_publishes
