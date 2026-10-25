"""Map garminconnect dicts to cairn.worker.v1 proto messages."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from google.protobuf import duration_pb2, timestamp_pb2

import cairn_garmin  # noqa: F401  (bootstraps the proto path)
from cairn.v1 import activity_pb2 as a
from cairn.v1 import gear_pb2 as g
from cairn.worker.v1 import worker_service_pb2 as w

JSON = dict[str, Any]

# Garmin typeKey → (ActivityType, Discipline, is_virtual).
_SPORT = {
    "running": (a.ACTIVITY_TYPE_RUN, a.DISCIPLINE_RUN_ROAD, False),
    "trail_running": (a.ACTIVITY_TYPE_RUN, a.DISCIPLINE_RUN_TRAIL, False),
    "track_running": (a.ACTIVITY_TYPE_RUN, a.DISCIPLINE_RUN_TRACK, False),
    "treadmill_running": (a.ACTIVITY_TYPE_RUN, a.DISCIPLINE_UNSPECIFIED, True),
    "cycling": (a.ACTIVITY_TYPE_RIDE, a.DISCIPLINE_RIDE_ROAD, False),
    "road_biking": (a.ACTIVITY_TYPE_RIDE, a.DISCIPLINE_RIDE_ROAD, False),
    "gravel_cycling": (a.ACTIVITY_TYPE_RIDE, a.DISCIPLINE_RIDE_GRAVEL, False),
    "mountain_biking": (a.ACTIVITY_TYPE_RIDE, a.DISCIPLINE_RIDE_MTB, False),
    "indoor_cycling": (a.ACTIVITY_TYPE_RIDE, a.DISCIPLINE_UNSPECIFIED, True),
    "virtual_ride": (a.ACTIVITY_TYPE_RIDE, a.DISCIPLINE_UNSPECIFIED, True),
    "lap_swimming": (a.ACTIVITY_TYPE_SWIM, a.DISCIPLINE_UNSPECIFIED, False),
    "open_water_swimming": (a.ACTIVITY_TYPE_SWIM, a.DISCIPLINE_UNSPECIFIED, False),
    "walking": (a.ACTIVITY_TYPE_WALK, a.DISCIPLINE_UNSPECIFIED, False),
    "hiking": (a.ACTIVITY_TYPE_HIKE, a.DISCIPLINE_UNSPECIFIED, False),
    "rowing": (a.ACTIVITY_TYPE_ROW, a.DISCIPLINE_UNSPECIFIED, False),
    "indoor_rowing": (a.ACTIVITY_TYPE_ROW, a.DISCIPLINE_UNSPECIFIED, True),
}


def _ts(epoch_ms: int | None) -> timestamp_pb2.Timestamp | None:
    if epoch_ms is None:
        return None
    t = timestamp_pb2.Timestamp()
    t.FromDatetime(datetime.fromtimestamp(epoch_ms / 1000, tz=UTC))
    return t


def _dur(seconds: float | None) -> duration_pb2.Duration | None:
    if seconds is None:
        return None
    d = duration_pb2.Duration()
    d.FromSeconds(int(seconds))
    return d


def _f(v: Any) -> float | None:
    return float(v) if isinstance(v, (int, float)) else None


def _i(v: Any) -> int | None:
    return int(v) if isinstance(v, (int, float)) else None


def _first(m: JSON, *keys: str) -> Any:
    for k in keys:
        if m.get(k) is not None:
            return m[k]
    return None


def _timezone(act: JSON) -> str:
    """IANA timezone from Garmin's varied shapes; UTC fallback (required field)."""
    tzu = act.get("timeZoneUnitDTO") or {}
    return str(tzu.get("timeZone") or tzu.get("unitKey") or act.get("timezone") or "UTC")


def start_ms(act: JSON) -> int | None:
    """Garmin start as epoch ms, from beginTimestamp (ms) or startTimeGMT (ISO)."""
    if isinstance(act.get("beginTimestamp"), (int, float)):
        return int(act["beginTimestamp"])
    raw = act.get("startTimeGMT") or (act.get("summaryDTO") or {}).get("startTimeGMT")
    if isinstance(raw, str) and raw:
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S"):
            try:
                return int(datetime.strptime(raw, fmt).replace(tzinfo=UTC).timestamp() * 1000)
            except ValueError:
                continue
    return None


def activity_payload(act: JSON) -> a.ActivitySourcePayload:
    # get_activities (list) is flat; get_activity nests under summaryDTO/activityTypeDTO.
    m = {**(act.get("summaryDTO") or {}), **act}
    type_key = ((act.get("activityType") or act.get("activityTypeDTO") or {}) or {}).get("typeKey", "")
    at, disc, virtual = _SPORT.get(type_key, (a.ACTIVITY_TYPE_WORKOUT, a.DISCIPLINE_UNSPECIFIED, False))

    p = a.ActivitySourcePayload(
        type=at,
        discipline=disc,
        is_virtual=virtual,
        provider_native_type=type_key,
        title=act.get("activityName") or "",
        description=act.get("description") or "",
        timezone=_timezone(act),
    )
    if at == a.ACTIVITY_TYPE_WORKOUT and type_key:
        p.custom_subtype = type_key

    begin_ms = start_ms(act)
    if start := _ts(begin_ms):
        p.start_time.CopyFrom(start)
    elapsed = _first(m, "elapsedDuration", "duration")
    moving = _first(m, "movingDuration", "duration")
    if d := _dur(elapsed):
        p.elapsed_duration.CopyFrom(d)
    if d := _dur(moving):
        p.moving_duration.CopyFrom(d)
    if begin_ms and elapsed and (end := _ts(int(begin_ms + elapsed * 1000))):
        p.end_time.CopyFrom(end)

    s = p.summary
    _set(s, "distance_m", _f(m.get("distance")))
    _set(s, "elevation_gain_m", _f(m.get("elevationGain")))
    _set(s, "elevation_loss_m", _f(m.get("elevationLoss")))
    _set(s, "min_elevation_m", _f(m.get("minElevation")))
    _set(s, "max_elevation_m", _f(m.get("maxElevation")))
    _set(s, "avg_speed_mps", _f(_first(m, "averageSpeed", "avgSpeed")))
    _set(s, "max_speed_mps", _f(m.get("maxSpeed")))
    _set(s, "avg_heart_rate_bpm", _i(_first(m, "averageHR", "avgHr")))
    _set(s, "max_heart_rate_bpm", _i(_first(m, "maxHR", "maxHr")))
    _set(s, "avg_power_w", _i(_first(m, "avgPower", "averagePower")))
    _set(s, "max_power_w", _i(m.get("maxPower")))
    _set(s, "normalized_power_w", _i(_first(m, "normPower", "normalizedPower")))
    _set(s, "calories_kcal", _i(m.get("calories")))
    _set(
        s,
        "avg_cadence",
        _i(
            _first(
                m,
                "averageRunningCadenceInStepsPerMinute",
                "averageBikingCadenceInRevPerMinute",
                "averageRunCadence",
            )
        ),
    )
    return p


def _set(summary: a.ActivitySummary, field: str, value: float | None) -> None:
    """Set an optional summary field only when present (proto optionals)."""
    if value is not None:
        setattr(summary, field, value)


# Garmin detail metric key → ActivityStream column + numeric coercion.
_CHANNELS = {
    "directLatitude": ("latitude", float),
    "directLongitude": ("longitude", float),
    "directElevation": ("altitude_m", float),
    "sumDistance": ("distance_m", float),
    "directSpeed": ("speed_mps", float),
    "directHeartRate": ("heart_rate_bpm", int),
    "directPower": ("power_w", int),
    "directBikeCadence": ("cadence", int),
    "directRunCadence": ("cadence", int),
    "directAirTemperature": ("temperature_c", float),
}
_CHANNEL_ENUM = {
    "latitude": a.STREAM_CHANNEL_LATITUDE,
    "longitude": a.STREAM_CHANNEL_LONGITUDE,
    "altitude_m": a.STREAM_CHANNEL_ALTITUDE,
    "distance_m": a.STREAM_CHANNEL_DISTANCE,
    "speed_mps": a.STREAM_CHANNEL_SPEED,
    "heart_rate_bpm": a.STREAM_CHANNEL_HEART_RATE,
    "power_w": a.STREAM_CHANNEL_POWER,
    "cadence": a.STREAM_CHANNEL_CADENCE,
    "temperature_c": a.STREAM_CHANNEL_TEMPERATURE,
}


def activity_stream(details: JSON, start_ms: int | None) -> a.ActivityStream | None:
    """Map get_activity_details() metric arrays to a column-oriented ActivityStream."""
    descriptors = details.get("metricDescriptors") or []
    metrics = details.get("activityDetailMetrics") or []
    if not descriptors or not metrics:
        return None

    ts_idx, idx_to_col = _stream_columns(descriptors)
    if ts_idx is not None:
        metrics = _dedupe_timestamps(metrics, ts_idx)

    # dict.fromkeys keeps descriptor order; a set made channel order vary per process.
    cols: dict[str, list[Any]] = {c: [] for c in dict.fromkeys(idx_to_col.values())}
    times: list[float] = []
    for row in metrics:
        vals = row.get("metrics") or []
        if ts_idx is not None and ts_idx < len(vals) and vals[ts_idx] and start_ms:
            times.append((vals[ts_idx] - start_ms) / 1000.0)
        for i, col in idx_to_col.items():
            cols[col].append(vals[i] if i < len(vals) else None)

    st = a.ActivityStream(sample_count=len(metrics), resolution_hz=1.0)
    if times:
        st.time_s.extend(times)
    _fill_columns(st, cols)
    if st.time_s:
        st.channels.append(a.STREAM_CHANNEL_TIME)
    return st


def _stream_columns(descriptors: list[JSON]) -> tuple[int | None, dict[int, str]]:
    """The timestamp's metricsIndex and metricsIndex → our column name."""
    idx_to_col: dict[int, str] = {}
    ts_idx: int | None = None
    for d in descriptors:
        key = d.get("key")
        i = d.get("metricsIndex")
        if not isinstance(i, int):
            continue
        if key == "directTimestamp":
            ts_idx = i
        elif key in _CHANNELS:
            idx_to_col[i] = _CHANNELS[key][0]
    return ts_idx, idx_to_col


def _dedupe_timestamps(metrics: list[JSON], ts_idx: int) -> list[JSON]:
    """Keep the last row per timestamp.

    Garmin details can repeat a timestamp (seen live on a Zwift-synced ride:
    3 of 1977 rows duplicated around a pause); the server's (source, ts)
    stream key must be unique.
    """
    last_by_ts: dict[Any, int] = {}
    deduped: list[JSON] = []
    for row in metrics:
        vals = row.get("metrics") or []
        ts = vals[ts_idx] if ts_idx < len(vals) else None
        if ts is None:
            deduped.append(row)
        elif ts in last_by_ts:
            deduped[last_by_ts[ts]] = row
        else:
            last_by_ts[ts] = len(deduped)
            deduped.append(row)
    return deduped


def _fill_columns(st: a.ActivityStream, cols: dict[str, list[Any]]) -> None:
    """Coerce each non-empty column and register its channel."""
    for col, values in cols.items():
        coerce = float if col not in ("heart_rate_bpm", "power_w", "cadence") else int
        cleaned = [coerce(v) for v in values if v is not None]
        if not cleaned:
            continue
        getattr(st, col).extend(cleaned)
        if col in _CHANNEL_ENUM:
            st.channels.append(_CHANNEL_ENUM[col])


# --- gear --------------------------------------------------------------------
#
# gear-service records: uuid (stable id), gearTypeName (Bike/Shoes/Other),
# gearStatusName (active/retired), displayName, customMakeModel,
# gearMakeName/gearModelName, maximumMeters. Defaults come as per-activity-type
# entries naming the gear uuid.

_GEAR_KIND = {"bike": g.GEAR_KIND_BIKE, "bikes": g.GEAR_KIND_BIKE, "shoe": g.GEAR_KIND_SHOE, "shoes": g.GEAR_KIND_SHOE}


def gear_name(rec: JSON) -> str:
    name = rec.get("displayName") or rec.get("customMakeModel")
    if not name:
        name = " ".join(str(v) for v in (rec.get("gearMakeName"), rec.get("gearModelName")) if v)
    return str(name or rec.get("uuid") or "")


def gear_import(rec: JSON, default_for: list[a.ActivityType] | None = None) -> w.GearImport:
    imp = w.GearImport(
        kind=_GEAR_KIND.get(str(rec.get("gearTypeName") or "").lower(), g.GEAR_KIND_OTHER),
        name=gear_name(rec),
        brand=str(rec.get("gearMakeName") or ""),
        model=str(rec.get("gearModelName") or ""),
        description=str(rec.get("notes") or ""),
        retired=str(rec.get("gearStatusName") or "").lower() == "retired",
        primary=bool(default_for),
    )
    if (dist := _f(rec.get("totalDistance"))) is not None:
        imp.distance_m = dist
    imp.default_for.extend(default_for or [])
    return imp


def gear_event(
    user_id: str, account_id: str, rec: JSON, default_for: list[a.ActivityType] | None = None
) -> w.WorkerEvent:
    ref = w.ExternalRef(
        user_id=user_id, provider="garmin", external_account_id=account_id, external_id=str(rec.get("uuid") or "")
    )
    return w.WorkerEvent(
        type=w.WORKER_EVENT_TYPE_GEAR, gear=w.ImportedGear(ref=ref, payload=gear_import(rec, default_for))
    )


def gear_default_types(defaults: list[JSON]) -> dict[str, list[a.ActivityType]]:
    """gear uuid → the ActivityTypes it is the default for (unknown typeKeys dropped)."""
    out: dict[str, list[a.ActivityType]] = {}
    for d in defaults:
        uuid = d.get("uuid") or d.get("gearUuid")
        key = d.get("activityTypeKey")
        if not key and isinstance(d.get("activityType"), dict):
            key = d["activityType"].get("typeKey")
        if not uuid or not key or d.get("defaultGear") is False:
            continue
        sport = _SPORT.get(str(key))
        if sport and sport[0] not in out.setdefault(str(uuid), []):
            out[str(uuid)].append(sport[0])
    return out


def apply_activity_gear(payload: a.ActivitySourcePayload, gear: list[JSON]) -> None:
    """The first gear recorded on the activity becomes the payload's reference."""
    for rec in gear:
        if rec.get("uuid"):
            payload.gear_external_id = str(rec["uuid"])
            payload.gear_name = gear_name(rec)
            return


def metric_event(user_id: str, account_id: str, key: str, day_ms: int, value: float) -> w.WorkerEvent:
    ts = timestamp_pb2.Timestamp()
    ts.FromDatetime(datetime.fromtimestamp(day_ms / 1000, tz=UTC))
    im = w.ImportedMetric(
        ref=w.ExternalRef(
            user_id=user_id, provider="garmin", external_account_id=account_id, external_id=f"{key}:{day_ms}"
        ),
        key=key,
        ts=ts,
        value_numeric=value,
    )
    return w.WorkerEvent(type=w.WORKER_EVENT_TYPE_METRIC, metric=im)


def job_result(events: list[w.WorkerEvent], *, name: str, version: str, package: str, release: str = "") -> w.JobResult:
    return w.JobResult(
        events=events, worker_name=name, worker_version=version, worker_package=package, worker_release=release
    )


def parse_archive(env: JSON, *, user_id: str, account_id: str, ext_id: str, blob_id: str = "") -> list[w.WorkerEvent]:
    """The parser proper: an archived envelope in, events out. Import and
    re-parse both run it, so a re-parse reproduces the import. Its output is
    pinned per parser version by tests/test_parser_golden.py.
    """
    act = env.get("activity") or {}
    details = env.get("details")
    # Absent (before parser 1.2) or None: the gear was not looked up, which is
    # not "no gear"; core keeps a previous import's gear.
    raw_gear = env.get("gear")
    gear = raw_gear or []
    ref = w.ExternalRef(user_id=user_id, provider="garmin", external_account_id=account_id, external_id=str(ext_id))
    imported = w.ImportedActivity(ref=ref, payload=activity_payload(act))
    if raw_gear is None:
        imported.payload.gear_unknown = True
    if details:
        stream = activity_stream(details, start_ms(act))
        if stream is not None:
            imported.stream.CopyFrom(stream)
    apply_activity_gear(imported.payload, gear)
    if blob_id:
        imported.raw_blob_id = blob_id
    # GEAR events precede the activity that references them.
    events = [gear_event(user_id, account_id, rec) for rec in gear if rec.get("uuid")]
    events.append(w.WorkerEvent(type=w.WORKER_EVENT_TYPE_ACTIVITY, activity=imported))
    return events
