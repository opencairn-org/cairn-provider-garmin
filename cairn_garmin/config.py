"""Worker configuration from environment."""

from __future__ import annotations

import os
import uuid
from dataclasses import dataclass, field
from pathlib import Path

# PROVIDER + PACKAGE + versions are compile-time identity (core ADR 0005),
# baked into the source, NOT env-overridable. DATASET_VERSION is the archive
# envelope format; bump it only when the parser can no longer read the previous
# one. VERSION is the parser version DATASET_VERSION.M: bump M with EVERY change
# to the parsed output (tests/test_parser_golden.py enforces it).
PROVIDER = "garmin"
PACKAGE = "cairn.workers.garmin"
DATASET_VERSION = 1
VERSION = "1.2"  # 1.1: gear id per activity; 1.2: gear read from the archive


def _read_release() -> str:
    """Release tag written into the image at build time (Dockerfile); "" in dev."""
    try:
        return (Path(__file__).with_name("RELEASE")).read_text().strip()
    except OSError:
        return ""


# Core requires the same major.minor (core ADR 0005).
RELEASE = _read_release()

# WORKER_NAME is the admin-defined routing identity (it must match the
# enrollment name) and is SHARED across every instance of this worker — so it is
# env-configurable, defaulting to "garmin-fetcher". Distinct from instance_id
# (below), which is per-instance.
WORKER_NAME = os.getenv("CAIRN_WORKER_NAME", "garmin-fetcher")

JOB_STREAM = "CAIRN_JOBS"
CORE_INFO_KV = "cairn_core"


def job_subject(job: str) -> str:
    """This pool's subject for a job kind (core ADR 0006)."""
    return f"cairn.jobs.{job}.{PROVIDER}.{WORKER_NAME}"


# Pre-0.5 provider-only subjects, drained once after the upgrade. Remove in 0.6.
def legacy_subject(job: str) -> str:
    return f"cairn.jobs.{job}.{PROVIDER}"


DISCOVER_SUBJECT = f"cairn.discover.{PROVIDER}.{WORKER_NAME}"
RESULT_SUBJECT = f"cairn.results.fetch_source.{PROVIDER}"
RESULT_METRICS = f"cairn.results.import_metrics.{PROVIDER}"
SUBJ_FETCH = job_subject("fetch_source")
SUBJ_METRICS = job_subject("import_metrics")
SUBJ_PARSE_BLOB = job_subject("parse_blob")
SUBJ_RECONCILE = job_subject("reconcile")
SUBJ_GEAR = job_subject("import_gear")
RESULT_GEAR = f"cairn.results.import_gear.{PROVIDER}"
# Reconcile results are account-suffixed so the server can attribute the
# watermark: cairn.results.reconcile.garmin.<external_account_id>.
RESULT_RECONCILE_PREFIX = f"cairn.results.reconcile.{PROVIDER}"
PRESIGN_DOWNLOAD_SUBJECT = f"cairn.blobs.presign_download.{PROVIDER}"
PRESENCE_KV = "cairn_worker_presence"


@dataclass
class Config:
    nats_url: str = field(default_factory=lambda: os.getenv("CAIRN_NATS_URL", "nats://localhost:4222"))
    # Per-instance id, only needs to be UNIQUE per running instance (it
    # disambiguates replicas of the same WORKER_NAME in presence/heartbeats).
    # Unset → a random uuid is generated; in k8s set it to the pod name so a
    # restart reuses the same presence key instead of leaving a ghost.
    instance_id: str = field(default_factory=lambda: os.getenv("CAIRN_WORKER_INSTANCE_ID", "") or uuid.uuid4().hex[:12])
    # Enrollment token from core; core's NATS auth-callout admits it scoped to this provider.
    enrollment_token: str = field(default_factory=lambda: os.getenv("CAIRN_WORKER_ENROLLMENT_TOKEN", ""))
    nats_user: str = field(default_factory=lambda: os.getenv("CAIRN_NATS_USER", ""))
    nats_password: str = field(default_factory=lambda: os.getenv("CAIRN_NATS_PASSWORD", ""))
    heartbeat_interval_s: int = field(default_factory=lambda: int(os.getenv("CAIRN_HEARTBEAT_INTERVAL_S", "20")))
    pull_batch: int = field(default_factory=lambda: int(os.getenv("CAIRN_PULL_BATCH", "4")))

    # Dev fallback Garmin credentials when the job carries none (single account).
    garmin_email: str = field(default_factory=lambda: os.getenv("CAIRN_GARMIN_EMAIL", ""))
    garmin_password: str = field(default_factory=lambda: os.getenv("CAIRN_GARMIN_PASSWORD", ""))
    # Garth token store dir (persists Garmin session so we don't log in every job).
    # Defaults to a per-user dir: the tokens are credentials, not for a shared /tmp.
    garth_home: str = field(
        default_factory=lambda: os.getenv("CAIRN_GARTH_HOME", os.path.expanduser("~/.cache/cairn-garth"))
    )
    # Per-activity gear costs one extra Garmin call per fetch; switch it off
    # for accounts that hit Garmin's (undocumented) limits.
    fetch_activity_gear: bool = field(
        default_factory=lambda: (
            os.getenv("CAIRN_GARMIN_FETCH_ACTIVITY_GEAR", "true").lower() not in ("0", "false", "no")
        )
    )


def load() -> Config:
    return Config()
