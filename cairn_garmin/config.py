"""Worker configuration from environment, on top of the SDK's settings."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from cairn_provider_sdk import Identity, Settings, read_release, worker_name
from cairn_provider_sdk import config as sdk_config

# PROVIDER + PACKAGE + versions are compile-time identity (core ADR 0005),
# baked into the source, NOT env-overridable. DATASET_VERSION is the archive
# envelope format; bump it only when the parser can no longer read the previous
# one. VERSION is the parser version DATASET_VERSION.M: bump M with EVERY change
# to the parsed output (tests/test_parser_golden.py enforces it).
PROVIDER = "garmin"
PACKAGE = "cairn.workers.garmin"
DATASET_VERSION = 1
VERSION = "1.2"  # 1.1: gear id per activity; 1.2: gear read from the archive

# Release tag written into the image at build time (Dockerfile); "" in dev.
# Core requires the same major.minor (core ADR 0005).
RELEASE = read_release(Path(__file__).with_name("RELEASE"))

# WORKER_NAME is the admin-defined routing identity (it must match the
# enrollment name) and is SHARED across every instance of this worker — so it is
# env-configurable, defaulting to "garmin-fetcher". Distinct from instance_id
# (below), which is per-instance.
WORKER_NAME = worker_name("garmin-fetcher")

IDENTITY = Identity(
    provider=PROVIDER,
    package=PACKAGE,
    version=VERSION,
    dataset_version=DATASET_VERSION,
    release=RELEASE,
    worker_name=WORKER_NAME,
)

JOB_STREAM = sdk_config.JOB_STREAM
CORE_INFO_KV = sdk_config.CORE_INFO_KV
PRESENCE_KV = sdk_config.PRESENCE_KV
# The manifest (parser version + how Garmin is connected) lives here; core
# stores its provider_meta and drives the connect form from it.
MANIFEST_KV = sdk_config.MANIFEST_KV


def job_subject(job: str) -> str:
    """This pool's subject for a job kind (core ADR 0006)."""
    return IDENTITY.job_subject(job)


DISCOVER_SUBJECT = IDENTITY.discover_subject
# Results are per pool (core ADR 0006): cairn.results.<job>.<provider>.<name>.
RESULT_SUBJECT = IDENTITY.result_subject("fetch_source")
RESULT_METRICS = IDENTITY.result_subject("import_metrics")
RESULT_GEAR = IDENTITY.result_subject("import_gear")
# Reconcile results are account-suffixed so the server can attribute the
# watermark: cairn.results.reconcile.garmin.<name>.<external_account_id>.
RESULT_RECONCILE_PREFIX = IDENTITY.result_subject("reconcile")
SUBJ_FETCH = job_subject("fetch_source")
SUBJ_METRICS = job_subject("import_metrics")
SUBJ_PARSE_BLOB = job_subject("parse_blob")
SUBJ_RECONCILE = job_subject("reconcile")
SUBJ_GEAR = job_subject("import_gear")
CREDS_SUBJECT = IDENTITY.creds_subject
PRESIGN_SUBJECT = IDENTITY.presign_upload_subject
PRESIGN_DOWNLOAD_SUBJECT = IDENTITY.presign_download_subject


@dataclass
class Config(Settings):
    """The SDK's NATS settings (CAIRN_NATS_URL, CAIRN_WORKER_ENROLLMENT_TOKEN,
    CAIRN_WORKER_INSTANCE_ID, ...) plus the Garmin-specific ones."""

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
