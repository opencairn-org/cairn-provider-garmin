import datetime

from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from cairn.v1 import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GearSetBy(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GEAR_SET_BY_UNSPECIFIED: _ClassVar[GearSetBy]
    GEAR_SET_BY_MERGE: _ClassVar[GearSetBy]
    GEAR_SET_BY_USER: _ClassVar[GearSetBy]

class ActivityType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ACTIVITY_TYPE_UNSPECIFIED: _ClassVar[ActivityType]
    ACTIVITY_TYPE_RIDE: _ClassVar[ActivityType]
    ACTIVITY_TYPE_RUN: _ClassVar[ActivityType]
    ACTIVITY_TYPE_SWIM: _ClassVar[ActivityType]
    ACTIVITY_TYPE_HIKE: _ClassVar[ActivityType]
    ACTIVITY_TYPE_WALK: _ClassVar[ActivityType]
    ACTIVITY_TYPE_ROW: _ClassVar[ActivityType]
    ACTIVITY_TYPE_SKI: _ClassVar[ActivityType]
    ACTIVITY_TYPE_WORKOUT: _ClassVar[ActivityType]
    ACTIVITY_TYPE_SNOWBOARD: _ClassVar[ActivityType]
    ACTIVITY_TYPE_SKATE: _ClassVar[ActivityType]
    ACTIVITY_TYPE_KAYAK: _ClassVar[ActivityType]
    ACTIVITY_TYPE_SUP: _ClassVar[ActivityType]
    ACTIVITY_TYPE_SURF: _ClassVar[ActivityType]
    ACTIVITY_TYPE_GOLF: _ClassVar[ActivityType]
    ACTIVITY_TYPE_CLIMB: _ClassVar[ActivityType]
    ACTIVITY_TYPE_TENNIS: _ClassVar[ActivityType]
    ACTIVITY_TYPE_ELLIPTICAL: _ClassVar[ActivityType]
    ACTIVITY_TYPE_WHEELCHAIR: _ClassVar[ActivityType]

class Discipline(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DISCIPLINE_UNSPECIFIED: _ClassVar[Discipline]
    DISCIPLINE_RIDE_ROAD: _ClassVar[Discipline]
    DISCIPLINE_RIDE_MTB: _ClassVar[Discipline]
    DISCIPLINE_RIDE_GRAVEL: _ClassVar[Discipline]
    DISCIPLINE_RIDE_CYCLOCROSS: _ClassVar[Discipline]
    DISCIPLINE_RIDE_TRACK: _ClassVar[Discipline]
    DISCIPLINE_RIDE_BMX: _ClassVar[Discipline]
    DISCIPLINE_RUN_ROAD: _ClassVar[Discipline]
    DISCIPLINE_RUN_TRAIL: _ClassVar[Discipline]
    DISCIPLINE_RUN_TRACK: _ClassVar[Discipline]
    DISCIPLINE_SWIM_POOL: _ClassVar[Discipline]
    DISCIPLINE_SWIM_OPEN_WATER: _ClassVar[Discipline]
    DISCIPLINE_SKI_ALPINE: _ClassVar[Discipline]
    DISCIPLINE_SKI_NORDIC: _ClassVar[Discipline]
    DISCIPLINE_SKI_TOURING: _ClassVar[Discipline]
    DISCIPLINE_SKI_BACKCOUNTRY: _ClassVar[Discipline]

class Privacy(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PRIVACY_UNSPECIFIED: _ClassVar[Privacy]
    PRIVACY_PRIVATE: _ClassVar[Privacy]
    PRIVACY_FOLLOWERS: _ClassVar[Privacy]
    PRIVACY_PUBLIC: _ClassVar[Privacy]

class ActivitySourceStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ACTIVITY_SOURCE_STATUS_UNSPECIFIED: _ClassVar[ActivitySourceStatus]
    ACTIVITY_SOURCE_STATUS_ACTIVE: _ClassVar[ActivitySourceStatus]
    ACTIVITY_SOURCE_STATUS_ORPHANED: _ClassVar[ActivitySourceStatus]
    ACTIVITY_SOURCE_STATUS_ACCOUNT_UNAVAILABLE: _ClassVar[ActivitySourceStatus]
    ACTIVITY_SOURCE_STATUS_DETACHED: _ClassVar[ActivitySourceStatus]

class ReimportStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    REIMPORT_STATUS_UNSPECIFIED: _ClassVar[ReimportStatus]
    REIMPORT_STATUS_CURRENT: _ClassVar[ReimportStatus]
    REIMPORT_STATUS_UPDATE_AVAILABLE: _ClassVar[ReimportStatus]
    REIMPORT_STATUS_UPDATING: _ClassVar[ReimportStatus]
    REIMPORT_STATUS_FAILED: _ClassVar[ReimportStatus]

class StreamChannel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STREAM_CHANNEL_UNSPECIFIED: _ClassVar[StreamChannel]
    STREAM_CHANNEL_TIME: _ClassVar[StreamChannel]
    STREAM_CHANNEL_LATITUDE: _ClassVar[StreamChannel]
    STREAM_CHANNEL_LONGITUDE: _ClassVar[StreamChannel]
    STREAM_CHANNEL_ALTITUDE: _ClassVar[StreamChannel]
    STREAM_CHANNEL_DISTANCE: _ClassVar[StreamChannel]
    STREAM_CHANNEL_SPEED: _ClassVar[StreamChannel]
    STREAM_CHANNEL_HEART_RATE: _ClassVar[StreamChannel]
    STREAM_CHANNEL_POWER: _ClassVar[StreamChannel]
    STREAM_CHANNEL_CADENCE: _ClassVar[StreamChannel]
    STREAM_CHANNEL_TEMPERATURE: _ClassVar[StreamChannel]
    STREAM_CHANNEL_GRADE: _ClassVar[StreamChannel]
    STREAM_CHANNEL_LEFT_RIGHT_BALANCE: _ClassVar[StreamChannel]
    STREAM_CHANNEL_LEFT_TORQUE_EFFECTIVENESS: _ClassVar[StreamChannel]
    STREAM_CHANNEL_RIGHT_TORQUE_EFFECTIVENESS: _ClassVar[StreamChannel]
    STREAM_CHANNEL_LEFT_PEDAL_SMOOTHNESS: _ClassVar[StreamChannel]
    STREAM_CHANNEL_RIGHT_PEDAL_SMOOTHNESS: _ClassVar[StreamChannel]
    STREAM_CHANNEL_VERTICAL_OSCILLATION: _ClassVar[StreamChannel]
    STREAM_CHANNEL_GROUND_CONTACT_TIME: _ClassVar[StreamChannel]
    STREAM_CHANNEL_STRIDE_LENGTH: _ClassVar[StreamChannel]
    STREAM_CHANNEL_RESPIRATION_RATE: _ClassVar[StreamChannel]
    STREAM_CHANNEL_CORE_TEMPERATURE: _ClassVar[StreamChannel]

class BestEffortMetric(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BEST_EFFORT_METRIC_UNSPECIFIED: _ClassVar[BestEffortMetric]
    BEST_EFFORT_METRIC_PACE: _ClassVar[BestEffortMetric]
    BEST_EFFORT_METRIC_SPEED: _ClassVar[BestEffortMetric]
    BEST_EFFORT_METRIC_POWER: _ClassVar[BestEffortMetric]
    BEST_EFFORT_METRIC_HEART_RATE: _ClassVar[BestEffortMetric]
    BEST_EFFORT_METRIC_VAM: _ClassVar[BestEffortMetric]

class BestEffortWindowKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BEST_EFFORT_WINDOW_KIND_UNSPECIFIED: _ClassVar[BestEffortWindowKind]
    BEST_EFFORT_WINDOW_KIND_DISTANCE: _ClassVar[BestEffortWindowKind]
    BEST_EFFORT_WINDOW_KIND_DURATION: _ClassVar[BestEffortWindowKind]

class ActivitySort(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ACTIVITY_SORT_UNSPECIFIED: _ClassVar[ActivitySort]
    ACTIVITY_SORT_START_TIME_DESC: _ClassVar[ActivitySort]
    ACTIVITY_SORT_START_TIME_ASC: _ClassVar[ActivitySort]
    ACTIVITY_SORT_DISTANCE_DESC: _ClassVar[ActivitySort]
    ACTIVITY_SORT_DURATION_DESC: _ClassVar[ActivitySort]

class ActivityEventType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ACTIVITY_EVENT_TYPE_UNSPECIFIED: _ClassVar[ActivityEventType]
    ACTIVITY_EVENT_TYPE_IMPORT_STARTED: _ClassVar[ActivityEventType]
    ACTIVITY_EVENT_TYPE_IMPORT_PROGRESS: _ClassVar[ActivityEventType]
    ACTIVITY_EVENT_TYPE_IMPORT_COMPLETED: _ClassVar[ActivityEventType]
    ACTIVITY_EVENT_TYPE_IMPORT_FAILED: _ClassVar[ActivityEventType]
    ACTIVITY_EVENT_TYPE_ACTIVITY_CREATED: _ClassVar[ActivityEventType]
    ACTIVITY_EVENT_TYPE_ACTIVITY_UPDATED: _ClassVar[ActivityEventType]
    ACTIVITY_EVENT_TYPE_ACTIVITY_DELETED: _ClassVar[ActivityEventType]
    ACTIVITY_EVENT_TYPE_SOURCE_ATTACHED: _ClassVar[ActivityEventType]
    ACTIVITY_EVENT_TYPE_SOURCE_DETACHED: _ClassVar[ActivityEventType]
    ACTIVITY_EVENT_TYPE_REIMPORT_STARTED: _ClassVar[ActivityEventType]
    ACTIVITY_EVENT_TYPE_REIMPORT_COMPLETED: _ClassVar[ActivityEventType]
    ACTIVITY_EVENT_TYPE_REIMPORT_FAILED: _ClassVar[ActivityEventType]
    ACTIVITY_EVENT_TYPE_NEW_PR: _ClassVar[ActivityEventType]
    ACTIVITY_EVENT_TYPE_SEGMENT_PR: _ClassVar[ActivityEventType]
GEAR_SET_BY_UNSPECIFIED: GearSetBy
GEAR_SET_BY_MERGE: GearSetBy
GEAR_SET_BY_USER: GearSetBy
ACTIVITY_TYPE_UNSPECIFIED: ActivityType
ACTIVITY_TYPE_RIDE: ActivityType
ACTIVITY_TYPE_RUN: ActivityType
ACTIVITY_TYPE_SWIM: ActivityType
ACTIVITY_TYPE_HIKE: ActivityType
ACTIVITY_TYPE_WALK: ActivityType
ACTIVITY_TYPE_ROW: ActivityType
ACTIVITY_TYPE_SKI: ActivityType
ACTIVITY_TYPE_WORKOUT: ActivityType
ACTIVITY_TYPE_SNOWBOARD: ActivityType
ACTIVITY_TYPE_SKATE: ActivityType
ACTIVITY_TYPE_KAYAK: ActivityType
ACTIVITY_TYPE_SUP: ActivityType
ACTIVITY_TYPE_SURF: ActivityType
ACTIVITY_TYPE_GOLF: ActivityType
ACTIVITY_TYPE_CLIMB: ActivityType
ACTIVITY_TYPE_TENNIS: ActivityType
ACTIVITY_TYPE_ELLIPTICAL: ActivityType
ACTIVITY_TYPE_WHEELCHAIR: ActivityType
DISCIPLINE_UNSPECIFIED: Discipline
DISCIPLINE_RIDE_ROAD: Discipline
DISCIPLINE_RIDE_MTB: Discipline
DISCIPLINE_RIDE_GRAVEL: Discipline
DISCIPLINE_RIDE_CYCLOCROSS: Discipline
DISCIPLINE_RIDE_TRACK: Discipline
DISCIPLINE_RIDE_BMX: Discipline
DISCIPLINE_RUN_ROAD: Discipline
DISCIPLINE_RUN_TRAIL: Discipline
DISCIPLINE_RUN_TRACK: Discipline
DISCIPLINE_SWIM_POOL: Discipline
DISCIPLINE_SWIM_OPEN_WATER: Discipline
DISCIPLINE_SKI_ALPINE: Discipline
DISCIPLINE_SKI_NORDIC: Discipline
DISCIPLINE_SKI_TOURING: Discipline
DISCIPLINE_SKI_BACKCOUNTRY: Discipline
PRIVACY_UNSPECIFIED: Privacy
PRIVACY_PRIVATE: Privacy
PRIVACY_FOLLOWERS: Privacy
PRIVACY_PUBLIC: Privacy
ACTIVITY_SOURCE_STATUS_UNSPECIFIED: ActivitySourceStatus
ACTIVITY_SOURCE_STATUS_ACTIVE: ActivitySourceStatus
ACTIVITY_SOURCE_STATUS_ORPHANED: ActivitySourceStatus
ACTIVITY_SOURCE_STATUS_ACCOUNT_UNAVAILABLE: ActivitySourceStatus
ACTIVITY_SOURCE_STATUS_DETACHED: ActivitySourceStatus
REIMPORT_STATUS_UNSPECIFIED: ReimportStatus
REIMPORT_STATUS_CURRENT: ReimportStatus
REIMPORT_STATUS_UPDATE_AVAILABLE: ReimportStatus
REIMPORT_STATUS_UPDATING: ReimportStatus
REIMPORT_STATUS_FAILED: ReimportStatus
STREAM_CHANNEL_UNSPECIFIED: StreamChannel
STREAM_CHANNEL_TIME: StreamChannel
STREAM_CHANNEL_LATITUDE: StreamChannel
STREAM_CHANNEL_LONGITUDE: StreamChannel
STREAM_CHANNEL_ALTITUDE: StreamChannel
STREAM_CHANNEL_DISTANCE: StreamChannel
STREAM_CHANNEL_SPEED: StreamChannel
STREAM_CHANNEL_HEART_RATE: StreamChannel
STREAM_CHANNEL_POWER: StreamChannel
STREAM_CHANNEL_CADENCE: StreamChannel
STREAM_CHANNEL_TEMPERATURE: StreamChannel
STREAM_CHANNEL_GRADE: StreamChannel
STREAM_CHANNEL_LEFT_RIGHT_BALANCE: StreamChannel
STREAM_CHANNEL_LEFT_TORQUE_EFFECTIVENESS: StreamChannel
STREAM_CHANNEL_RIGHT_TORQUE_EFFECTIVENESS: StreamChannel
STREAM_CHANNEL_LEFT_PEDAL_SMOOTHNESS: StreamChannel
STREAM_CHANNEL_RIGHT_PEDAL_SMOOTHNESS: StreamChannel
STREAM_CHANNEL_VERTICAL_OSCILLATION: StreamChannel
STREAM_CHANNEL_GROUND_CONTACT_TIME: StreamChannel
STREAM_CHANNEL_STRIDE_LENGTH: StreamChannel
STREAM_CHANNEL_RESPIRATION_RATE: StreamChannel
STREAM_CHANNEL_CORE_TEMPERATURE: StreamChannel
BEST_EFFORT_METRIC_UNSPECIFIED: BestEffortMetric
BEST_EFFORT_METRIC_PACE: BestEffortMetric
BEST_EFFORT_METRIC_SPEED: BestEffortMetric
BEST_EFFORT_METRIC_POWER: BestEffortMetric
BEST_EFFORT_METRIC_HEART_RATE: BestEffortMetric
BEST_EFFORT_METRIC_VAM: BestEffortMetric
BEST_EFFORT_WINDOW_KIND_UNSPECIFIED: BestEffortWindowKind
BEST_EFFORT_WINDOW_KIND_DISTANCE: BestEffortWindowKind
BEST_EFFORT_WINDOW_KIND_DURATION: BestEffortWindowKind
ACTIVITY_SORT_UNSPECIFIED: ActivitySort
ACTIVITY_SORT_START_TIME_DESC: ActivitySort
ACTIVITY_SORT_START_TIME_ASC: ActivitySort
ACTIVITY_SORT_DISTANCE_DESC: ActivitySort
ACTIVITY_SORT_DURATION_DESC: ActivitySort
ACTIVITY_EVENT_TYPE_UNSPECIFIED: ActivityEventType
ACTIVITY_EVENT_TYPE_IMPORT_STARTED: ActivityEventType
ACTIVITY_EVENT_TYPE_IMPORT_PROGRESS: ActivityEventType
ACTIVITY_EVENT_TYPE_IMPORT_COMPLETED: ActivityEventType
ACTIVITY_EVENT_TYPE_IMPORT_FAILED: ActivityEventType
ACTIVITY_EVENT_TYPE_ACTIVITY_CREATED: ActivityEventType
ACTIVITY_EVENT_TYPE_ACTIVITY_UPDATED: ActivityEventType
ACTIVITY_EVENT_TYPE_ACTIVITY_DELETED: ActivityEventType
ACTIVITY_EVENT_TYPE_SOURCE_ATTACHED: ActivityEventType
ACTIVITY_EVENT_TYPE_SOURCE_DETACHED: ActivityEventType
ACTIVITY_EVENT_TYPE_REIMPORT_STARTED: ActivityEventType
ACTIVITY_EVENT_TYPE_REIMPORT_COMPLETED: ActivityEventType
ACTIVITY_EVENT_TYPE_REIMPORT_FAILED: ActivityEventType
ACTIVITY_EVENT_TYPE_NEW_PR: ActivityEventType
ACTIVITY_EVENT_TYPE_SEGMENT_PR: ActivityEventType

class Activity(_message.Message):
    __slots__ = ("id", "user_id", "type", "discipline", "is_virtual", "is_ebike", "is_commute", "is_race", "custom_subtype", "title", "description", "start_time", "end_time", "elapsed_duration", "moving_duration", "timezone", "summary", "sources", "primary_stream_source_id", "merge_provenance", "merged_at", "created_at", "updated_at", "tags", "gear_id", "privacy", "deleted_at", "start_place", "start_lat", "start_lng", "gear_set_by", "gear_name")
    class MergeProvenanceEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DISCIPLINE_FIELD_NUMBER: _ClassVar[int]
    IS_VIRTUAL_FIELD_NUMBER: _ClassVar[int]
    IS_EBIKE_FIELD_NUMBER: _ClassVar[int]
    IS_COMMUTE_FIELD_NUMBER: _ClassVar[int]
    IS_RACE_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_SUBTYPE_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    ELAPSED_DURATION_FIELD_NUMBER: _ClassVar[int]
    MOVING_DURATION_FIELD_NUMBER: _ClassVar[int]
    TIMEZONE_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    SOURCES_FIELD_NUMBER: _ClassVar[int]
    PRIMARY_STREAM_SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    MERGE_PROVENANCE_FIELD_NUMBER: _ClassVar[int]
    MERGED_AT_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    GEAR_ID_FIELD_NUMBER: _ClassVar[int]
    PRIVACY_FIELD_NUMBER: _ClassVar[int]
    DELETED_AT_FIELD_NUMBER: _ClassVar[int]
    START_PLACE_FIELD_NUMBER: _ClassVar[int]
    START_LAT_FIELD_NUMBER: _ClassVar[int]
    START_LNG_FIELD_NUMBER: _ClassVar[int]
    GEAR_SET_BY_FIELD_NUMBER: _ClassVar[int]
    GEAR_NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    user_id: str
    type: ActivityType
    discipline: Discipline
    is_virtual: bool
    is_ebike: bool
    is_commute: bool
    is_race: bool
    custom_subtype: str
    title: str
    description: str
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    elapsed_duration: _duration_pb2.Duration
    moving_duration: _duration_pb2.Duration
    timezone: str
    summary: ActivitySummary
    sources: _containers.RepeatedCompositeFieldContainer[ActivitySource]
    primary_stream_source_id: str
    merge_provenance: _containers.ScalarMap[str, str]
    merged_at: _timestamp_pb2.Timestamp
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    tags: _containers.RepeatedScalarFieldContainer[str]
    gear_id: str
    privacy: Privacy
    deleted_at: _timestamp_pb2.Timestamp
    start_place: str
    start_lat: float
    start_lng: float
    gear_set_by: GearSetBy
    gear_name: str
    def __init__(self, id: _Optional[str] = ..., user_id: _Optional[str] = ..., type: _Optional[_Union[ActivityType, str]] = ..., discipline: _Optional[_Union[Discipline, str]] = ..., is_virtual: _Optional[bool] = ..., is_ebike: _Optional[bool] = ..., is_commute: _Optional[bool] = ..., is_race: _Optional[bool] = ..., custom_subtype: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., start_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., elapsed_duration: _Optional[_Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]] = ..., moving_duration: _Optional[_Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]] = ..., timezone: _Optional[str] = ..., summary: _Optional[_Union[ActivitySummary, _Mapping]] = ..., sources: _Optional[_Iterable[_Union[ActivitySource, _Mapping]]] = ..., primary_stream_source_id: _Optional[str] = ..., merge_provenance: _Optional[_Mapping[str, str]] = ..., merged_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., tags: _Optional[_Iterable[str]] = ..., gear_id: _Optional[str] = ..., privacy: _Optional[_Union[Privacy, str]] = ..., deleted_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., start_place: _Optional[str] = ..., start_lat: _Optional[float] = ..., start_lng: _Optional[float] = ..., gear_set_by: _Optional[_Union[GearSetBy, str]] = ..., gear_name: _Optional[str] = ...) -> None: ...

class ActivitySummary(_message.Message):
    __slots__ = ("distance_m", "elevation_gain_m", "elevation_loss_m", "min_elevation_m", "max_elevation_m", "avg_speed_mps", "max_speed_mps", "avg_heart_rate_bpm", "max_heart_rate_bpm", "avg_power_w", "max_power_w", "normalized_power_w", "avg_cadence", "max_cadence", "avg_temperature_c", "min_temperature_c", "max_temperature_c", "calories_kcal", "tss", "intensity_factor", "pool_length_m", "total_strokes")
    DISTANCE_M_FIELD_NUMBER: _ClassVar[int]
    ELEVATION_GAIN_M_FIELD_NUMBER: _ClassVar[int]
    ELEVATION_LOSS_M_FIELD_NUMBER: _ClassVar[int]
    MIN_ELEVATION_M_FIELD_NUMBER: _ClassVar[int]
    MAX_ELEVATION_M_FIELD_NUMBER: _ClassVar[int]
    AVG_SPEED_MPS_FIELD_NUMBER: _ClassVar[int]
    MAX_SPEED_MPS_FIELD_NUMBER: _ClassVar[int]
    AVG_HEART_RATE_BPM_FIELD_NUMBER: _ClassVar[int]
    MAX_HEART_RATE_BPM_FIELD_NUMBER: _ClassVar[int]
    AVG_POWER_W_FIELD_NUMBER: _ClassVar[int]
    MAX_POWER_W_FIELD_NUMBER: _ClassVar[int]
    NORMALIZED_POWER_W_FIELD_NUMBER: _ClassVar[int]
    AVG_CADENCE_FIELD_NUMBER: _ClassVar[int]
    MAX_CADENCE_FIELD_NUMBER: _ClassVar[int]
    AVG_TEMPERATURE_C_FIELD_NUMBER: _ClassVar[int]
    MIN_TEMPERATURE_C_FIELD_NUMBER: _ClassVar[int]
    MAX_TEMPERATURE_C_FIELD_NUMBER: _ClassVar[int]
    CALORIES_KCAL_FIELD_NUMBER: _ClassVar[int]
    TSS_FIELD_NUMBER: _ClassVar[int]
    INTENSITY_FACTOR_FIELD_NUMBER: _ClassVar[int]
    POOL_LENGTH_M_FIELD_NUMBER: _ClassVar[int]
    TOTAL_STROKES_FIELD_NUMBER: _ClassVar[int]
    distance_m: float
    elevation_gain_m: float
    elevation_loss_m: float
    min_elevation_m: float
    max_elevation_m: float
    avg_speed_mps: float
    max_speed_mps: float
    avg_heart_rate_bpm: int
    max_heart_rate_bpm: int
    avg_power_w: int
    max_power_w: int
    normalized_power_w: int
    avg_cadence: int
    max_cadence: int
    avg_temperature_c: float
    min_temperature_c: float
    max_temperature_c: float
    calories_kcal: int
    tss: float
    intensity_factor: float
    pool_length_m: int
    total_strokes: int
    def __init__(self, distance_m: _Optional[float] = ..., elevation_gain_m: _Optional[float] = ..., elevation_loss_m: _Optional[float] = ..., min_elevation_m: _Optional[float] = ..., max_elevation_m: _Optional[float] = ..., avg_speed_mps: _Optional[float] = ..., max_speed_mps: _Optional[float] = ..., avg_heart_rate_bpm: _Optional[int] = ..., max_heart_rate_bpm: _Optional[int] = ..., avg_power_w: _Optional[int] = ..., max_power_w: _Optional[int] = ..., normalized_power_w: _Optional[int] = ..., avg_cadence: _Optional[int] = ..., max_cadence: _Optional[int] = ..., avg_temperature_c: _Optional[float] = ..., min_temperature_c: _Optional[float] = ..., max_temperature_c: _Optional[float] = ..., calories_kcal: _Optional[int] = ..., tss: _Optional[float] = ..., intensity_factor: _Optional[float] = ..., pool_length_m: _Optional[int] = ..., total_strokes: _Optional[int] = ...) -> None: ...

class ActivitySource(_message.Message):
    __slots__ = ("id", "activity_id", "provider", "external_account_id", "external_id", "source_worker_name", "source_worker_version", "source_worker_package", "raw_blob_id", "raw_content_type", "raw_size_bytes", "parsed", "status", "status_reason", "reimport_status", "reimport_status_reason", "imported_at", "last_reimported_at", "updated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_WORKER_NAME_FIELD_NUMBER: _ClassVar[int]
    SOURCE_WORKER_VERSION_FIELD_NUMBER: _ClassVar[int]
    SOURCE_WORKER_PACKAGE_FIELD_NUMBER: _ClassVar[int]
    RAW_BLOB_ID_FIELD_NUMBER: _ClassVar[int]
    RAW_CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    RAW_SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    PARSED_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STATUS_REASON_FIELD_NUMBER: _ClassVar[int]
    REIMPORT_STATUS_FIELD_NUMBER: _ClassVar[int]
    REIMPORT_STATUS_REASON_FIELD_NUMBER: _ClassVar[int]
    IMPORTED_AT_FIELD_NUMBER: _ClassVar[int]
    LAST_REIMPORTED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    activity_id: str
    provider: str
    external_account_id: str
    external_id: str
    source_worker_name: str
    source_worker_version: str
    source_worker_package: str
    raw_blob_id: str
    raw_content_type: str
    raw_size_bytes: int
    parsed: ActivitySourcePayload
    status: ActivitySourceStatus
    status_reason: str
    reimport_status: ReimportStatus
    reimport_status_reason: str
    imported_at: _timestamp_pb2.Timestamp
    last_reimported_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., activity_id: _Optional[str] = ..., provider: _Optional[str] = ..., external_account_id: _Optional[str] = ..., external_id: _Optional[str] = ..., source_worker_name: _Optional[str] = ..., source_worker_version: _Optional[str] = ..., source_worker_package: _Optional[str] = ..., raw_blob_id: _Optional[str] = ..., raw_content_type: _Optional[str] = ..., raw_size_bytes: _Optional[int] = ..., parsed: _Optional[_Union[ActivitySourcePayload, _Mapping]] = ..., status: _Optional[_Union[ActivitySourceStatus, str]] = ..., status_reason: _Optional[str] = ..., reimport_status: _Optional[_Union[ReimportStatus, str]] = ..., reimport_status_reason: _Optional[str] = ..., imported_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., last_reimported_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ActivitySourcePayload(_message.Message):
    __slots__ = ("type", "discipline", "is_virtual", "is_ebike", "provider_native_type", "is_commute", "is_race", "custom_subtype", "title", "description", "start_time", "end_time", "elapsed_duration", "moving_duration", "timezone", "summary", "laps", "stream_summary", "provider_segment_efforts", "provider_best_efforts", "extra", "gear_external_id", "gear_name", "gear_unknown")
    class ExtraEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DISCIPLINE_FIELD_NUMBER: _ClassVar[int]
    IS_VIRTUAL_FIELD_NUMBER: _ClassVar[int]
    IS_EBIKE_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_NATIVE_TYPE_FIELD_NUMBER: _ClassVar[int]
    IS_COMMUTE_FIELD_NUMBER: _ClassVar[int]
    IS_RACE_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_SUBTYPE_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    ELAPSED_DURATION_FIELD_NUMBER: _ClassVar[int]
    MOVING_DURATION_FIELD_NUMBER: _ClassVar[int]
    TIMEZONE_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    LAPS_FIELD_NUMBER: _ClassVar[int]
    STREAM_SUMMARY_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_SEGMENT_EFFORTS_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_BEST_EFFORTS_FIELD_NUMBER: _ClassVar[int]
    EXTRA_FIELD_NUMBER: _ClassVar[int]
    GEAR_EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    GEAR_NAME_FIELD_NUMBER: _ClassVar[int]
    GEAR_UNKNOWN_FIELD_NUMBER: _ClassVar[int]
    type: ActivityType
    discipline: Discipline
    is_virtual: bool
    is_ebike: bool
    provider_native_type: str
    is_commute: bool
    is_race: bool
    custom_subtype: str
    title: str
    description: str
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    elapsed_duration: _duration_pb2.Duration
    moving_duration: _duration_pb2.Duration
    timezone: str
    summary: ActivitySummary
    laps: _containers.RepeatedCompositeFieldContainer[ActivityLap]
    stream_summary: StreamSummary
    provider_segment_efforts: _containers.RepeatedCompositeFieldContainer[ProviderSegmentEffort]
    provider_best_efforts: _containers.RepeatedCompositeFieldContainer[ProviderBestEffort]
    extra: _containers.ScalarMap[str, str]
    gear_external_id: str
    gear_name: str
    gear_unknown: bool
    def __init__(self, type: _Optional[_Union[ActivityType, str]] = ..., discipline: _Optional[_Union[Discipline, str]] = ..., is_virtual: _Optional[bool] = ..., is_ebike: _Optional[bool] = ..., provider_native_type: _Optional[str] = ..., is_commute: _Optional[bool] = ..., is_race: _Optional[bool] = ..., custom_subtype: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., start_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., elapsed_duration: _Optional[_Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]] = ..., moving_duration: _Optional[_Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]] = ..., timezone: _Optional[str] = ..., summary: _Optional[_Union[ActivitySummary, _Mapping]] = ..., laps: _Optional[_Iterable[_Union[ActivityLap, _Mapping]]] = ..., stream_summary: _Optional[_Union[StreamSummary, _Mapping]] = ..., provider_segment_efforts: _Optional[_Iterable[_Union[ProviderSegmentEffort, _Mapping]]] = ..., provider_best_efforts: _Optional[_Iterable[_Union[ProviderBestEffort, _Mapping]]] = ..., extra: _Optional[_Mapping[str, str]] = ..., gear_external_id: _Optional[str] = ..., gear_name: _Optional[str] = ..., gear_unknown: _Optional[bool] = ...) -> None: ...

class ActivityLap(_message.Message):
    __slots__ = ("index", "start_time", "elapsed_duration", "moving_duration", "distance_m", "avg_heart_rate_bpm", "max_heart_rate_bpm", "avg_power_w", "max_power_w", "avg_speed_mps", "avg_cadence", "elevation_gain_m", "label")
    INDEX_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    ELAPSED_DURATION_FIELD_NUMBER: _ClassVar[int]
    MOVING_DURATION_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_M_FIELD_NUMBER: _ClassVar[int]
    AVG_HEART_RATE_BPM_FIELD_NUMBER: _ClassVar[int]
    MAX_HEART_RATE_BPM_FIELD_NUMBER: _ClassVar[int]
    AVG_POWER_W_FIELD_NUMBER: _ClassVar[int]
    MAX_POWER_W_FIELD_NUMBER: _ClassVar[int]
    AVG_SPEED_MPS_FIELD_NUMBER: _ClassVar[int]
    AVG_CADENCE_FIELD_NUMBER: _ClassVar[int]
    ELEVATION_GAIN_M_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    index: int
    start_time: _timestamp_pb2.Timestamp
    elapsed_duration: _duration_pb2.Duration
    moving_duration: _duration_pb2.Duration
    distance_m: float
    avg_heart_rate_bpm: int
    max_heart_rate_bpm: int
    avg_power_w: int
    max_power_w: int
    avg_speed_mps: float
    avg_cadence: int
    elevation_gain_m: float
    label: str
    def __init__(self, index: _Optional[int] = ..., start_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., elapsed_duration: _Optional[_Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]] = ..., moving_duration: _Optional[_Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]] = ..., distance_m: _Optional[float] = ..., avg_heart_rate_bpm: _Optional[int] = ..., max_heart_rate_bpm: _Optional[int] = ..., avg_power_w: _Optional[int] = ..., max_power_w: _Optional[int] = ..., avg_speed_mps: _Optional[float] = ..., avg_cadence: _Optional[int] = ..., elevation_gain_m: _Optional[float] = ..., label: _Optional[str] = ...) -> None: ...

class StreamSummary(_message.Message):
    __slots__ = ("channels", "sample_count", "sample_rate_hz", "has_gps", "polyline")
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_COUNT_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_RATE_HZ_FIELD_NUMBER: _ClassVar[int]
    HAS_GPS_FIELD_NUMBER: _ClassVar[int]
    POLYLINE_FIELD_NUMBER: _ClassVar[int]
    channels: _containers.RepeatedScalarFieldContainer[StreamChannel]
    sample_count: int
    sample_rate_hz: float
    has_gps: bool
    polyline: _common_pb2.EncodedPolyline
    def __init__(self, channels: _Optional[_Iterable[_Union[StreamChannel, str]]] = ..., sample_count: _Optional[int] = ..., sample_rate_hz: _Optional[float] = ..., has_gps: _Optional[bool] = ..., polyline: _Optional[_Union[_common_pb2.EncodedPolyline, _Mapping]] = ...) -> None: ...

class ProviderSegmentEffort(_message.Message):
    __slots__ = ("provider_segment_id", "segment_name", "start_time", "elapsed", "start_index", "end_index")
    PROVIDER_SEGMENT_ID_FIELD_NUMBER: _ClassVar[int]
    SEGMENT_NAME_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    ELAPSED_FIELD_NUMBER: _ClassVar[int]
    START_INDEX_FIELD_NUMBER: _ClassVar[int]
    END_INDEX_FIELD_NUMBER: _ClassVar[int]
    provider_segment_id: str
    segment_name: str
    start_time: _timestamp_pb2.Timestamp
    elapsed: _duration_pb2.Duration
    start_index: int
    end_index: int
    def __init__(self, provider_segment_id: _Optional[str] = ..., segment_name: _Optional[str] = ..., start_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., elapsed: _Optional[_Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]] = ..., start_index: _Optional[int] = ..., end_index: _Optional[int] = ...) -> None: ...

class ProviderBestEffort(_message.Message):
    __slots__ = ("name", "elapsed", "distance_m", "start_index", "end_index")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ELAPSED_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_M_FIELD_NUMBER: _ClassVar[int]
    START_INDEX_FIELD_NUMBER: _ClassVar[int]
    END_INDEX_FIELD_NUMBER: _ClassVar[int]
    name: str
    elapsed: _duration_pb2.Duration
    distance_m: float
    start_index: int
    end_index: int
    def __init__(self, name: _Optional[str] = ..., elapsed: _Optional[_Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]] = ..., distance_m: _Optional[float] = ..., start_index: _Optional[int] = ..., end_index: _Optional[int] = ...) -> None: ...

class ActivityStream(_message.Message):
    __slots__ = ("activity_source_id", "channels", "sample_count", "resolution_hz", "time_s", "latitude", "longitude", "altitude_m", "distance_m", "speed_mps", "heart_rate_bpm", "power_w", "cadence", "temperature_c", "grade")
    ACTIVITY_SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_COUNT_FIELD_NUMBER: _ClassVar[int]
    RESOLUTION_HZ_FIELD_NUMBER: _ClassVar[int]
    TIME_S_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    ALTITUDE_M_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_M_FIELD_NUMBER: _ClassVar[int]
    SPEED_MPS_FIELD_NUMBER: _ClassVar[int]
    HEART_RATE_BPM_FIELD_NUMBER: _ClassVar[int]
    POWER_W_FIELD_NUMBER: _ClassVar[int]
    CADENCE_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_C_FIELD_NUMBER: _ClassVar[int]
    GRADE_FIELD_NUMBER: _ClassVar[int]
    activity_source_id: str
    channels: _containers.RepeatedScalarFieldContainer[StreamChannel]
    sample_count: int
    resolution_hz: float
    time_s: _containers.RepeatedScalarFieldContainer[float]
    latitude: _containers.RepeatedScalarFieldContainer[float]
    longitude: _containers.RepeatedScalarFieldContainer[float]
    altitude_m: _containers.RepeatedScalarFieldContainer[float]
    distance_m: _containers.RepeatedScalarFieldContainer[float]
    speed_mps: _containers.RepeatedScalarFieldContainer[float]
    heart_rate_bpm: _containers.RepeatedScalarFieldContainer[int]
    power_w: _containers.RepeatedScalarFieldContainer[int]
    cadence: _containers.RepeatedScalarFieldContainer[int]
    temperature_c: _containers.RepeatedScalarFieldContainer[float]
    grade: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, activity_source_id: _Optional[str] = ..., channels: _Optional[_Iterable[_Union[StreamChannel, str]]] = ..., sample_count: _Optional[int] = ..., resolution_hz: _Optional[float] = ..., time_s: _Optional[_Iterable[float]] = ..., latitude: _Optional[_Iterable[float]] = ..., longitude: _Optional[_Iterable[float]] = ..., altitude_m: _Optional[_Iterable[float]] = ..., distance_m: _Optional[_Iterable[float]] = ..., speed_mps: _Optional[_Iterable[float]] = ..., heart_rate_bpm: _Optional[_Iterable[int]] = ..., power_w: _Optional[_Iterable[int]] = ..., cadence: _Optional[_Iterable[int]] = ..., temperature_c: _Optional[_Iterable[float]] = ..., grade: _Optional[_Iterable[float]] = ...) -> None: ...

class BestEffort(_message.Message):
    __slots__ = ("id", "activity_id", "user_id", "activity_type", "discipline", "metric", "window_kind", "window_value", "achieved_value", "start_offset", "duration", "distance_m", "ts", "activity_source_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_TYPE_FIELD_NUMBER: _ClassVar[int]
    DISCIPLINE_FIELD_NUMBER: _ClassVar[int]
    METRIC_FIELD_NUMBER: _ClassVar[int]
    WINDOW_KIND_FIELD_NUMBER: _ClassVar[int]
    WINDOW_VALUE_FIELD_NUMBER: _ClassVar[int]
    ACHIEVED_VALUE_FIELD_NUMBER: _ClassVar[int]
    START_OFFSET_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_M_FIELD_NUMBER: _ClassVar[int]
    TS_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    activity_id: str
    user_id: str
    activity_type: ActivityType
    discipline: Discipline
    metric: BestEffortMetric
    window_kind: BestEffortWindowKind
    window_value: int
    achieved_value: float
    start_offset: int
    duration: _duration_pb2.Duration
    distance_m: float
    ts: _timestamp_pb2.Timestamp
    activity_source_id: str
    def __init__(self, id: _Optional[str] = ..., activity_id: _Optional[str] = ..., user_id: _Optional[str] = ..., activity_type: _Optional[_Union[ActivityType, str]] = ..., discipline: _Optional[_Union[Discipline, str]] = ..., metric: _Optional[_Union[BestEffortMetric, str]] = ..., window_kind: _Optional[_Union[BestEffortWindowKind, str]] = ..., window_value: _Optional[int] = ..., achieved_value: _Optional[float] = ..., start_offset: _Optional[int] = ..., duration: _Optional[_Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]] = ..., distance_m: _Optional[float] = ..., ts: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., activity_source_id: _Optional[str] = ...) -> None: ...

class UserRecord(_message.Message):
    __slots__ = ("user_id", "activity_type", "discipline", "metric", "window_kind", "window_value", "achieved_value", "activity_id", "activity_source_id", "best_effort_id", "ts", "previous_value", "previous_ts")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_TYPE_FIELD_NUMBER: _ClassVar[int]
    DISCIPLINE_FIELD_NUMBER: _ClassVar[int]
    METRIC_FIELD_NUMBER: _ClassVar[int]
    WINDOW_KIND_FIELD_NUMBER: _ClassVar[int]
    WINDOW_VALUE_FIELD_NUMBER: _ClassVar[int]
    ACHIEVED_VALUE_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    BEST_EFFORT_ID_FIELD_NUMBER: _ClassVar[int]
    TS_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_VALUE_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_TS_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    activity_type: ActivityType
    discipline: Discipline
    metric: BestEffortMetric
    window_kind: BestEffortWindowKind
    window_value: int
    achieved_value: float
    activity_id: str
    activity_source_id: str
    best_effort_id: str
    ts: _timestamp_pb2.Timestamp
    previous_value: float
    previous_ts: _timestamp_pb2.Timestamp
    def __init__(self, user_id: _Optional[str] = ..., activity_type: _Optional[_Union[ActivityType, str]] = ..., discipline: _Optional[_Union[Discipline, str]] = ..., metric: _Optional[_Union[BestEffortMetric, str]] = ..., window_kind: _Optional[_Union[BestEffortWindowKind, str]] = ..., window_value: _Optional[int] = ..., achieved_value: _Optional[float] = ..., activity_id: _Optional[str] = ..., activity_source_id: _Optional[str] = ..., best_effort_id: _Optional[str] = ..., ts: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., previous_value: _Optional[float] = ..., previous_ts: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class CustomBestEffort(_message.Message):
    __slots__ = ("id", "user_id", "activity_type", "metric", "window_kind", "window_value", "label", "created_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_TYPE_FIELD_NUMBER: _ClassVar[int]
    METRIC_FIELD_NUMBER: _ClassVar[int]
    WINDOW_KIND_FIELD_NUMBER: _ClassVar[int]
    WINDOW_VALUE_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    user_id: str
    activity_type: ActivityType
    metric: BestEffortMetric
    window_kind: BestEffortWindowKind
    window_value: int
    label: str
    created_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., user_id: _Optional[str] = ..., activity_type: _Optional[_Union[ActivityType, str]] = ..., metric: _Optional[_Union[BestEffortMetric, str]] = ..., window_kind: _Optional[_Union[BestEffortWindowKind, str]] = ..., window_value: _Optional[int] = ..., label: _Optional[str] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ListActivitiesRequest(_message.Message):
    __slots__ = ("time_range", "types", "disciplines", "providers", "tags", "sort", "page", "include_sources")
    TIME_RANGE_FIELD_NUMBER: _ClassVar[int]
    TYPES_FIELD_NUMBER: _ClassVar[int]
    DISCIPLINES_FIELD_NUMBER: _ClassVar[int]
    PROVIDERS_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    SORT_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_SOURCES_FIELD_NUMBER: _ClassVar[int]
    time_range: _common_pb2.TimeRange
    types: _containers.RepeatedScalarFieldContainer[ActivityType]
    disciplines: _containers.RepeatedScalarFieldContainer[Discipline]
    providers: _containers.RepeatedScalarFieldContainer[str]
    tags: _containers.RepeatedScalarFieldContainer[str]
    sort: ActivitySort
    page: _common_pb2.PageRequest
    include_sources: bool
    def __init__(self, time_range: _Optional[_Union[_common_pb2.TimeRange, _Mapping]] = ..., types: _Optional[_Iterable[_Union[ActivityType, str]]] = ..., disciplines: _Optional[_Iterable[_Union[Discipline, str]]] = ..., providers: _Optional[_Iterable[str]] = ..., tags: _Optional[_Iterable[str]] = ..., sort: _Optional[_Union[ActivitySort, str]] = ..., page: _Optional[_Union[_common_pb2.PageRequest, _Mapping]] = ..., include_sources: _Optional[bool] = ...) -> None: ...

class ListActivitiesResponse(_message.Message):
    __slots__ = ("activities", "page")
    ACTIVITIES_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    activities: _containers.RepeatedCompositeFieldContainer[Activity]
    page: _common_pb2.PageResponse
    def __init__(self, activities: _Optional[_Iterable[_Union[Activity, _Mapping]]] = ..., page: _Optional[_Union[_common_pb2.PageResponse, _Mapping]] = ...) -> None: ...

class GetActivityRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetActivityResponse(_message.Message):
    __slots__ = ("activity",)
    ACTIVITY_FIELD_NUMBER: _ClassVar[int]
    activity: Activity
    def __init__(self, activity: _Optional[_Union[Activity, _Mapping]] = ...) -> None: ...

class UpdateActivityRequest(_message.Message):
    __slots__ = ("id", "field_mask", "title", "description", "type", "discipline", "is_virtual", "is_commute", "is_race", "is_ebike", "custom_subtype", "tags", "privacy", "primary_stream_source_id", "distance_m", "elevation_gain_m", "moving_duration_s", "gear_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    FIELD_MASK_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DISCIPLINE_FIELD_NUMBER: _ClassVar[int]
    IS_VIRTUAL_FIELD_NUMBER: _ClassVar[int]
    IS_COMMUTE_FIELD_NUMBER: _ClassVar[int]
    IS_RACE_FIELD_NUMBER: _ClassVar[int]
    IS_EBIKE_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_SUBTYPE_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    PRIVACY_FIELD_NUMBER: _ClassVar[int]
    PRIMARY_STREAM_SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_M_FIELD_NUMBER: _ClassVar[int]
    ELEVATION_GAIN_M_FIELD_NUMBER: _ClassVar[int]
    MOVING_DURATION_S_FIELD_NUMBER: _ClassVar[int]
    GEAR_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    field_mask: _containers.RepeatedScalarFieldContainer[str]
    title: str
    description: str
    type: ActivityType
    discipline: Discipline
    is_virtual: bool
    is_commute: bool
    is_race: bool
    is_ebike: bool
    custom_subtype: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    privacy: Privacy
    primary_stream_source_id: str
    distance_m: float
    elevation_gain_m: float
    moving_duration_s: int
    gear_id: str
    def __init__(self, id: _Optional[str] = ..., field_mask: _Optional[_Iterable[str]] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., type: _Optional[_Union[ActivityType, str]] = ..., discipline: _Optional[_Union[Discipline, str]] = ..., is_virtual: _Optional[bool] = ..., is_commute: _Optional[bool] = ..., is_race: _Optional[bool] = ..., is_ebike: _Optional[bool] = ..., custom_subtype: _Optional[str] = ..., tags: _Optional[_Iterable[str]] = ..., privacy: _Optional[_Union[Privacy, str]] = ..., primary_stream_source_id: _Optional[str] = ..., distance_m: _Optional[float] = ..., elevation_gain_m: _Optional[float] = ..., moving_duration_s: _Optional[int] = ..., gear_id: _Optional[str] = ...) -> None: ...

class UpdateActivityResponse(_message.Message):
    __slots__ = ("activity",)
    ACTIVITY_FIELD_NUMBER: _ClassVar[int]
    activity: Activity
    def __init__(self, activity: _Optional[_Union[Activity, _Mapping]] = ...) -> None: ...

class DeleteActivityRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteActivityResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class StreamActivityEventsRequest(_message.Message):
    __slots__ = ("types",)
    TYPES_FIELD_NUMBER: _ClassVar[int]
    types: _containers.RepeatedScalarFieldContainer[ActivityEventType]
    def __init__(self, types: _Optional[_Iterable[_Union[ActivityEventType, str]]] = ...) -> None: ...

class ActivityEvent(_message.Message):
    __slots__ = ("type", "ts", "activity_id", "activity_source_id", "i18n_key", "i18n_params", "progress", "items_done", "items_total")
    class I18nParamsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TS_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    I18N_KEY_FIELD_NUMBER: _ClassVar[int]
    I18N_PARAMS_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    ITEMS_DONE_FIELD_NUMBER: _ClassVar[int]
    ITEMS_TOTAL_FIELD_NUMBER: _ClassVar[int]
    type: ActivityEventType
    ts: _timestamp_pb2.Timestamp
    activity_id: str
    activity_source_id: str
    i18n_key: str
    i18n_params: _containers.ScalarMap[str, str]
    progress: float
    items_done: int
    items_total: int
    def __init__(self, type: _Optional[_Union[ActivityEventType, str]] = ..., ts: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., activity_id: _Optional[str] = ..., activity_source_id: _Optional[str] = ..., i18n_key: _Optional[str] = ..., i18n_params: _Optional[_Mapping[str, str]] = ..., progress: _Optional[float] = ..., items_done: _Optional[int] = ..., items_total: _Optional[int] = ...) -> None: ...

class ListActivitySourcesRequest(_message.Message):
    __slots__ = ("activity_id",)
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: str
    def __init__(self, activity_id: _Optional[str] = ...) -> None: ...

class ListActivitySourcesResponse(_message.Message):
    __slots__ = ("sources",)
    SOURCES_FIELD_NUMBER: _ClassVar[int]
    sources: _containers.RepeatedCompositeFieldContainer[ActivitySource]
    def __init__(self, sources: _Optional[_Iterable[_Union[ActivitySource, _Mapping]]] = ...) -> None: ...

class ReimportSourceRequest(_message.Message):
    __slots__ = ("activity_source_id", "prefer_local_reparse")
    ACTIVITY_SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    PREFER_LOCAL_REPARSE_FIELD_NUMBER: _ClassVar[int]
    activity_source_id: str
    prefer_local_reparse: bool
    def __init__(self, activity_source_id: _Optional[str] = ..., prefer_local_reparse: _Optional[bool] = ...) -> None: ...

class ReimportSourceResponse(_message.Message):
    __slots__ = ("job_id",)
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    def __init__(self, job_id: _Optional[str] = ...) -> None: ...

class PreviewSourceReimportRequest(_message.Message):
    __slots__ = ("activity_source_id", "prefer_local_reparse")
    ACTIVITY_SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    PREFER_LOCAL_REPARSE_FIELD_NUMBER: _ClassVar[int]
    activity_source_id: str
    prefer_local_reparse: bool
    def __init__(self, activity_source_id: _Optional[str] = ..., prefer_local_reparse: _Optional[bool] = ...) -> None: ...

class PreviewSourceReimportResponse(_message.Message):
    __slots__ = ("preview_id", "job_id")
    PREVIEW_ID_FIELD_NUMBER: _ClassVar[int]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    preview_id: str
    job_id: str
    def __init__(self, preview_id: _Optional[str] = ..., job_id: _Optional[str] = ...) -> None: ...

class CommitSourcePreviewRequest(_message.Message):
    __slots__ = ("preview_id",)
    PREVIEW_ID_FIELD_NUMBER: _ClassVar[int]
    preview_id: str
    def __init__(self, preview_id: _Optional[str] = ...) -> None: ...

class CommitSourcePreviewResponse(_message.Message):
    __slots__ = ("activity",)
    ACTIVITY_FIELD_NUMBER: _ClassVar[int]
    activity: Activity
    def __init__(self, activity: _Optional[_Union[Activity, _Mapping]] = ...) -> None: ...

class DiscardSourcePreviewRequest(_message.Message):
    __slots__ = ("preview_id",)
    PREVIEW_ID_FIELD_NUMBER: _ClassVar[int]
    preview_id: str
    def __init__(self, preview_id: _Optional[str] = ...) -> None: ...

class DiscardSourcePreviewResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class LinkSourceToActivityRequest(_message.Message):
    __slots__ = ("activity_source_id", "target_activity_id", "force")
    ACTIVITY_SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    FORCE_FIELD_NUMBER: _ClassVar[int]
    activity_source_id: str
    target_activity_id: str
    force: bool
    def __init__(self, activity_source_id: _Optional[str] = ..., target_activity_id: _Optional[str] = ..., force: _Optional[bool] = ...) -> None: ...

class LinkSourceToActivityResponse(_message.Message):
    __slots__ = ("activity",)
    ACTIVITY_FIELD_NUMBER: _ClassVar[int]
    activity: Activity
    def __init__(self, activity: _Optional[_Union[Activity, _Mapping]] = ...) -> None: ...

class DetachSourceRequest(_message.Message):
    __slots__ = ("activity_source_id", "keep_as_new_activity")
    ACTIVITY_SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    KEEP_AS_NEW_ACTIVITY_FIELD_NUMBER: _ClassVar[int]
    activity_source_id: str
    keep_as_new_activity: bool
    def __init__(self, activity_source_id: _Optional[str] = ..., keep_as_new_activity: _Optional[bool] = ...) -> None: ...

class DetachSourceResponse(_message.Message):
    __slots__ = ("new_activity",)
    NEW_ACTIVITY_FIELD_NUMBER: _ClassVar[int]
    new_activity: Activity
    def __init__(self, new_activity: _Optional[_Union[Activity, _Mapping]] = ...) -> None: ...

class GetActivityStreamRequest(_message.Message):
    __slots__ = ("activity_source_id", "channels", "max_resolution_hz", "max_samples")
    ACTIVITY_SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    MAX_RESOLUTION_HZ_FIELD_NUMBER: _ClassVar[int]
    MAX_SAMPLES_FIELD_NUMBER: _ClassVar[int]
    activity_source_id: str
    channels: _containers.RepeatedScalarFieldContainer[StreamChannel]
    max_resolution_hz: float
    max_samples: int
    def __init__(self, activity_source_id: _Optional[str] = ..., channels: _Optional[_Iterable[_Union[StreamChannel, str]]] = ..., max_resolution_hz: _Optional[float] = ..., max_samples: _Optional[int] = ...) -> None: ...

class GetActivityStreamResponse(_message.Message):
    __slots__ = ("stream",)
    STREAM_FIELD_NUMBER: _ClassVar[int]
    stream: ActivityStream
    def __init__(self, stream: _Optional[_Union[ActivityStream, _Mapping]] = ...) -> None: ...

class PresignActivityUploadRequest(_message.Message):
    __slots__ = ("extension", "content_type", "size_hint_bytes")
    EXTENSION_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    SIZE_HINT_BYTES_FIELD_NUMBER: _ClassVar[int]
    extension: str
    content_type: str
    size_hint_bytes: int
    def __init__(self, extension: _Optional[str] = ..., content_type: _Optional[str] = ..., size_hint_bytes: _Optional[int] = ...) -> None: ...

class PresignActivityUploadResponse(_message.Message):
    __slots__ = ("blob_id", "upload_url", "required_headers", "expires_at")
    class RequiredHeadersEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    BLOB_ID_FIELD_NUMBER: _ClassVar[int]
    UPLOAD_URL_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_HEADERS_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    blob_id: str
    upload_url: str
    required_headers: _containers.ScalarMap[str, str]
    expires_at: _timestamp_pb2.Timestamp
    def __init__(self, blob_id: _Optional[str] = ..., upload_url: _Optional[str] = ..., required_headers: _Optional[_Mapping[str, str]] = ..., expires_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class UploadActivityRequest(_message.Message):
    __slots__ = ("blob_id", "filename", "content_type", "type_hint", "discipline_hint", "tags")
    BLOB_ID_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    TYPE_HINT_FIELD_NUMBER: _ClassVar[int]
    DISCIPLINE_HINT_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    blob_id: str
    filename: str
    content_type: str
    type_hint: ActivityType
    discipline_hint: Discipline
    tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, blob_id: _Optional[str] = ..., filename: _Optional[str] = ..., content_type: _Optional[str] = ..., type_hint: _Optional[_Union[ActivityType, str]] = ..., discipline_hint: _Optional[_Union[Discipline, str]] = ..., tags: _Optional[_Iterable[str]] = ...) -> None: ...

class UploadActivityResponse(_message.Message):
    __slots__ = ("job_id", "activity_id")
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    activity_id: str
    def __init__(self, job_id: _Optional[str] = ..., activity_id: _Optional[str] = ...) -> None: ...

class ListBestEffortsRequest(_message.Message):
    __slots__ = ("activity_id", "metrics")
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    activity_id: str
    metrics: _containers.RepeatedScalarFieldContainer[BestEffortMetric]
    def __init__(self, activity_id: _Optional[str] = ..., metrics: _Optional[_Iterable[_Union[BestEffortMetric, str]]] = ...) -> None: ...

class ListBestEffortsResponse(_message.Message):
    __slots__ = ("efforts",)
    EFFORTS_FIELD_NUMBER: _ClassVar[int]
    efforts: _containers.RepeatedCompositeFieldContainer[BestEffort]
    def __init__(self, efforts: _Optional[_Iterable[_Union[BestEffort, _Mapping]]] = ...) -> None: ...

class ListRecordsRequest(_message.Message):
    __slots__ = ("activity_type", "discipline", "time_range", "metrics")
    ACTIVITY_TYPE_FIELD_NUMBER: _ClassVar[int]
    DISCIPLINE_FIELD_NUMBER: _ClassVar[int]
    TIME_RANGE_FIELD_NUMBER: _ClassVar[int]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    activity_type: ActivityType
    discipline: Discipline
    time_range: _common_pb2.TimeRange
    metrics: _containers.RepeatedScalarFieldContainer[BestEffortMetric]
    def __init__(self, activity_type: _Optional[_Union[ActivityType, str]] = ..., discipline: _Optional[_Union[Discipline, str]] = ..., time_range: _Optional[_Union[_common_pb2.TimeRange, _Mapping]] = ..., metrics: _Optional[_Iterable[_Union[BestEffortMetric, str]]] = ...) -> None: ...

class ListRecordsResponse(_message.Message):
    __slots__ = ("records",)
    RECORDS_FIELD_NUMBER: _ClassVar[int]
    records: _containers.RepeatedCompositeFieldContainer[UserRecord]
    def __init__(self, records: _Optional[_Iterable[_Union[UserRecord, _Mapping]]] = ...) -> None: ...

class CreateCustomBestEffortRequest(_message.Message):
    __slots__ = ("activity_type", "metric", "window_kind", "window_value", "label")
    ACTIVITY_TYPE_FIELD_NUMBER: _ClassVar[int]
    METRIC_FIELD_NUMBER: _ClassVar[int]
    WINDOW_KIND_FIELD_NUMBER: _ClassVar[int]
    WINDOW_VALUE_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    activity_type: ActivityType
    metric: BestEffortMetric
    window_kind: BestEffortWindowKind
    window_value: int
    label: str
    def __init__(self, activity_type: _Optional[_Union[ActivityType, str]] = ..., metric: _Optional[_Union[BestEffortMetric, str]] = ..., window_kind: _Optional[_Union[BestEffortWindowKind, str]] = ..., window_value: _Optional[int] = ..., label: _Optional[str] = ...) -> None: ...

class CreateCustomBestEffortResponse(_message.Message):
    __slots__ = ("custom_best_effort",)
    CUSTOM_BEST_EFFORT_FIELD_NUMBER: _ClassVar[int]
    custom_best_effort: CustomBestEffort
    def __init__(self, custom_best_effort: _Optional[_Union[CustomBestEffort, _Mapping]] = ...) -> None: ...

class DeleteCustomBestEffortRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteCustomBestEffortResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
