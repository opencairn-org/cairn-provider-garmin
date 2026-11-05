"""Shared fakes for runtime tests: the SDK's in-memory NATS/JetStream stubs and
a Garmin Worker built without a NATS connection."""

from typing import cast

from cairn_provider_sdk.testing import FakeJS, FakeKV, FakeMsg, FakeNC, FakePullSub, Responder, as_nats
from cairn_provider_sdk.testing import make_worker as sdk_make_worker

from cairn_garmin import config as C
from cairn_garmin import runtime
from cairn_garmin.garmin_client import GarminClient

__all__ = ["FakeJS", "FakeKV", "FakeMsg", "FakeNC", "FakePullSub", "Responder", "as_nats", "make_worker"]


def make_worker(
    client: object | None = None,
    account_id: str = "acc-1",
    nc: FakeNC | None = None,
    cfg: C.Config | None = None,
) -> tuple[runtime.Worker, FakeJS]:
    """A Worker wired to a FakeJS; `client` duck-types GarminClient."""
    wk, js = sdk_make_worker(
        runtime.Worker(cfg or C.Config(garmin_email="", garmin_password="", garth_home="/nonexistent")), nc
    )
    wk._clients = {account_id: cast(GarminClient, client)} if client is not None else {}
    return wk, js
