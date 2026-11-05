"""Garmin capability manifest (advertised in the presence heartbeat) and the
provider meta core builds the connect flow from (published in the manifest KV).

Garmin's value over Strava is health data: HRV, sleep, weight, steps, resting HR.
Keys are canonical DataType identifiers (internal/domain/capability).
"""

from __future__ import annotations

from typing import Any


def provider_meta() -> dict[str, Any]:
    """How Garmin is connected: by Garmin Connect login, no OAuth round-trip."""
    return {
        "display_name": "Garmin",
        "activity_url_template": "https://connect.garmin.com/modern/activity/{id}",
        "setup_docs_url": "https://docs.opencairn.org/self-host/providers/garmin",
        "auth_method": "credentials",
        "config_fields": [
            {"key": "client_id", "label": "Garmin Connect email"},
            {
                "key": "client_secret",
                "label": "Password",
                "secret": True,
                "help": (
                    "Garmin has no public API, so Cairn signs in with your Garmin Connect email and "
                    "password (stored encrypted). MFA accounts may need a one-time device approval. "
                    "The account starts importing right after you create the connection."
                ),
            },
        ],
    }


def manifest() -> dict[str, dict[str, bool | str]]:
    return {
        "Activity": {"read": True, "backfill": True, "granularity": "per-activity"},
        "HRV": {"read": True, "backfill": True, "granularity": "daily"},
        "Sleep": {"read": True, "backfill": True, "granularity": "daily"},
        "Weight": {"read": True, "backfill": True, "granularity": "daily"},
        "Steps": {"read": True, "backfill": True, "granularity": "daily"},
        "RestingHR": {"read": True, "backfill": True, "granularity": "daily"},
        "Gear": {"read": True, "backfill": True, "granularity": "per-account"},
    }
