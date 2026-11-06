"""Mapping tests: garminconnect dicts → cairn.worker.v1 proto."""

from typing import Any

from cairn.v1 import activity_pb2 as a

from cairn_garmin import mapping

# --- start_ms ----------------------------------------------------------------


def test_start_ms_from_begin_timestamp() -> None:
    assert mapping.start_ms({"beginTimestamp": 1700000000000}) == 1700000000000


def test_start_ms_from_iso_gmt_variants() -> None:
    assert mapping.start_ms({"startTimeGMT": "2024-09-08 06:30:00"}) is not None
    nested = {"summaryDTO": {"startTimeGMT": "2024-09-08T06:30:00.0"}}
    assert mapping.start_ms(nested) is not None


def test_start_ms_absent() -> None:
    assert mapping.start_ms({}) is None
    assert mapping.start_ms({"startTimeGMT": "not-a-date"}) is None


# --- timezone (required field, UTC fallback) ---------------------------------


def test_timezone_prefers_explicit_then_falls_back() -> None:
    assert mapping._timezone({"timeZoneUnitDTO": {"timeZone": "Europe/Berlin"}}) == "Europe/Berlin"
    assert mapping._timezone({"timeZoneUnitDTO": {"unitKey": "Europe/Paris"}}) == "Europe/Paris"
    assert mapping._timezone({"timezone": "America/New_York"}) == "America/New_York"
    assert mapping._timezone({}) == "UTC"


# --- activity_payload --------------------------------------------------------


def test_payload_nested_get_activity_shape() -> None:
    act = {
        "activityName": "Morning Ride",
        "description": "easy spin",
        "activityTypeDTO": {"typeKey": "road_biking"},
        "timeZoneUnitDTO": {"timeZone": "Europe/Berlin"},
        "beginTimestamp": 1700000000000,
        "summaryDTO": {
            "distance": 30000.0,
            "duration": 3600.0,
            "movingDuration": 3500.0,
            "averageSpeed": 8.3,
            "averageHR": 142,
            "maxHR": 175,
            "avgPower": 210,
            "elevationGain": 250.0,
            "calories": 800,
            "averageBikingCadenceInRevPerMinute": 88,
        },
    }
    p = mapping.activity_payload(act)
    assert p.type == a.ACTIVITY_TYPE_RIDE
    assert p.discipline == a.DISCIPLINE_RIDE_ROAD
    assert p.title == "Morning Ride"
    assert p.timezone == "Europe/Berlin"
    assert p.provider_native_type == "road_biking"
    assert p.summary.distance_m == 30000.0
    assert p.summary.avg_heart_rate_bpm == 142
    assert p.summary.avg_power_w == 210
    assert p.summary.avg_cadence == 88
    assert p.HasField("start_time")
    assert p.HasField("end_time")  # begin + elapsed


def test_payload_flat_list_shape() -> None:
    # get_activities (list) returns flat fields, no summaryDTO nesting.
    act = {
        "activityName": "Run",
        "activityType": {"typeKey": "running"},
        "startTimeGMT": "2024-09-08 06:30:00",
        "distance": 10000.0,
        "duration": 3000.0,
        "averageHR": 150,
        "averageRunningCadenceInStepsPerMinute": 170,
    }
    p = mapping.activity_payload(act)
    assert p.type == a.ACTIVITY_TYPE_RUN
    assert p.discipline == a.DISCIPLINE_RUN_ROAD
    assert p.summary.distance_m == 10000.0
    assert p.summary.avg_heart_rate_bpm == 150
    assert p.summary.avg_cadence == 170


def test_payload_unknown_sport_is_workout_with_custom_subtype() -> None:
    p = mapping.activity_payload({"activityType": {"typeKey": "yoga"}, "activityName": "Stretch"})
    assert p.type == a.ACTIVITY_TYPE_WORKOUT
    assert p.custom_subtype == "yoga"
    assert p.provider_native_type == "yoga"


def test_payload_virtual_flag() -> None:
    p = mapping.activity_payload({"activityType": {"typeKey": "indoor_cycling"}})
    assert p.type == a.ACTIVITY_TYPE_RIDE
    assert p.is_virtual is True


# --- activity_stream ---------------------------------------------------------


def _details(rows: list[dict[str, Any]], descriptors: list[dict[str, Any]]) -> dict[str, Any]:
    return {"metricDescriptors": descriptors, "activityDetailMetrics": rows}


def test_stream_pivots_columns_and_coerces_types() -> None:
    descriptors = [
        {"key": "directTimestamp", "metricsIndex": 0},
        {"key": "directLatitude", "metricsIndex": 1},
        {"key": "directLongitude", "metricsIndex": 2},
        {"key": "directHeartRate", "metricsIndex": 3},
        {"key": "directPower", "metricsIndex": 4},
    ]
    start = 1700000000000
    rows = [
        {"metrics": [start + 0, 52.5, 13.4, 120.0, 200.0]},
        {"metrics": [start + 1000, 52.6, 13.5, 130.0, 210.0]},
    ]
    st = mapping.activity_stream(_details(rows, descriptors), start)
    assert st is not None
    assert st.sample_count == 2
    assert list(st.latitude) == [52.5, 52.6]
    # HR/power coerce to int
    assert list(st.heart_rate_bpm) == [120, 130]
    assert list(st.power_w) == [200, 210]
    # time offsets in seconds relative to start
    assert list(st.time_s) == [0.0, 1.0]
    assert a.STREAM_CHANNEL_HEART_RATE in st.channels
    assert a.STREAM_CHANNEL_TIME in st.channels


def test_stream_empty_when_no_metrics() -> None:
    assert mapping.activity_stream({"metricDescriptors": [], "activityDetailMetrics": []}, 0) is None
    assert mapping.activity_stream({}, 0) is None


def test_stream_skips_all_none_channel() -> None:
    descriptors = [
        {"key": "directTimestamp", "metricsIndex": 0},
        {"key": "directHeartRate", "metricsIndex": 1},
        {"key": "directPower", "metricsIndex": 2},
    ]
    start = 1700000000000
    rows = [{"metrics": [start, 120.0, None]}, {"metrics": [start + 1000, 130.0, None]}]
    st = mapping.activity_stream(_details(rows, descriptors), start)
    assert st is not None
    assert list(st.heart_rate_bpm) == [120, 130]
    assert len(st.power_w) == 0
    assert a.STREAM_CHANNEL_POWER not in st.channels


# --- metric_event ------------------------------------------------------------


def test_metric_event_external_id_format() -> None:
    ev = mapping.metric_event("u1", "acc1", "RestingHR", 1700000000000, 48.0)
    assert ev.metric.key == "RestingHR"
    assert ev.metric.value_numeric == 48.0
    assert ev.metric.ref.external_id == "RestingHR:1700000000000"
    assert ev.metric.ref.provider == "garmin"


def test_activity_stream_dedupes_duplicate_timestamps() -> None:
    # Seen live (Zwift ride 15258731664): Garmin details repeated 3 of 1977
    # timestamps; the server's (source, ts) stream key requires uniqueness.
    details = {
        "metricDescriptors": [
            {"key": "directTimestamp", "metricsIndex": 0},
            {"key": "directPower", "metricsIndex": 1},
        ],
        "activityDetailMetrics": [
            {"metrics": [1000.0, 100]},
            {"metrics": [2000.0, 110]},
            {"metrics": [2000.0, 120]},  # duplicate ts — last row wins
            {"metrics": [3000.0, 130]},
        ],
    }
    st = mapping.activity_stream(details, 1000)
    assert st is not None
    assert st.sample_count == 3
    assert list(st.time_s) == [0.0, 1.0, 2.0]
    assert list(st.power_w) == [100, 120, 130]


def test_stream_ignores_descriptors_without_index() -> None:
    descriptors: list[dict[str, Any]] = [
        {"key": "directTimestamp", "metricsIndex": 0},
        {"key": "directHeartRate"},
        {"key": "directPower", "metricsIndex": 1},
    ]
    st = mapping.activity_stream(_details([{"metrics": [1000, 200.0]}], descriptors), 1000)
    assert st is not None
    assert list(st.power_w) == [200]
    assert list(st.heart_rate_bpm) == []
