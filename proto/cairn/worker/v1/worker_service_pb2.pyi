import datetime

from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from cairn.v1 import activity_pb2 as _activity_pb2
from cairn.v1 import gear_pb2 as _gear_pb2
from cairn.v1 import segment_pb2 as _segment_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class WorkerEventType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WORKER_EVENT_TYPE_UNSPECIFIED: _ClassVar[WorkerEventType]
    WORKER_EVENT_TYPE_ACTIVITY: _ClassVar[WorkerEventType]
    WORKER_EVENT_TYPE_SEGMENT: _ClassVar[WorkerEventType]
    WORKER_EVENT_TYPE_SEGMENT_EFFORT: _ClassVar[WorkerEventType]
    WORKER_EVENT_TYPE_RECORD: _ClassVar[WorkerEventType]
    WORKER_EVENT_TYPE_METRIC: _ClassVar[WorkerEventType]
    WORKER_EVENT_TYPE_GEAR: _ClassVar[WorkerEventType]

class AuthMethod(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AUTH_METHOD_UNSPECIFIED: _ClassVar[AuthMethod]
    AUTH_METHOD_NONE: _ClassVar[AuthMethod]
    AUTH_METHOD_OAUTH2: _ClassVar[AuthMethod]
    AUTH_METHOD_API_KEY: _ClassVar[AuthMethod]
    AUTH_METHOD_BASIC: _ClassVar[AuthMethod]
    AUTH_METHOD_CUSTOM: _ClassVar[AuthMethod]

class FieldType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FIELD_TYPE_UNSPECIFIED: _ClassVar[FieldType]
    FIELD_TYPE_TEXT: _ClassVar[FieldType]
    FIELD_TYPE_SECRET: _ClassVar[FieldType]
    FIELD_TYPE_URL: _ClassVar[FieldType]
    FIELD_TYPE_NUMBER: _ClassVar[FieldType]
    FIELD_TYPE_BOOL: _ClassVar[FieldType]
    FIELD_TYPE_SELECT: _ClassVar[FieldType]
    FIELD_TYPE_MULTI_SELECT: _ClassVar[FieldType]
    FIELD_TYPE_DATE: _ClassVar[FieldType]

class JobType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    JOB_TYPE_UNSPECIFIED: _ClassVar[JobType]
    JOB_TYPE_IMPORT_ACTIVITIES: _ClassVar[JobType]
    JOB_TYPE_REIMPORT_ACTIVITY: _ClassVar[JobType]
    JOB_TYPE_LOCAL_REPARSE: _ClassVar[JobType]
    JOB_TYPE_IMPORT_SEGMENTS: _ClassVar[JobType]
    JOB_TYPE_FETCH_SEGMENT_DETAIL: _ClassVar[JobType]
    JOB_TYPE_IMPORT_METRICS: _ClassVar[JobType]
    JOB_TYPE_REGISTER_WEBHOOK: _ClassVar[JobType]
    JOB_TYPE_UNREGISTER_WEBHOOK: _ClassVar[JobType]
    JOB_TYPE_VALIDATE_CREDENTIALS: _ClassVar[JobType]
    JOB_TYPE_REFRESH_OAUTH_TOKEN: _ClassVar[JobType]
    JOB_TYPE_IMPORT_GEAR: _ClassVar[JobType]

class ReportInstruction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    REPORT_INSTRUCTION_UNSPECIFIED: _ClassVar[ReportInstruction]
    REPORT_INSTRUCTION_NONE: _ClassVar[ReportInstruction]
    REPORT_INSTRUCTION_ACK: _ClassVar[ReportInstruction]
    REPORT_INSTRUCTION_PAUSE_PROVIDER: _ClassVar[ReportInstruction]

class JobStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    JOB_STATUS_UNSPECIFIED: _ClassVar[JobStatus]
    JOB_STATUS_OK: _ClassVar[JobStatus]
    JOB_STATUS_FAILED: _ClassVar[JobStatus]
    JOB_STATUS_RATE_LIMITED: _ClassVar[JobStatus]
    JOB_STATUS_AUTH_EXPIRED: _ClassVar[JobStatus]
    JOB_STATUS_RETRYABLE: _ClassVar[JobStatus]
    JOB_STATUS_PROVIDER_DOWN: _ClassVar[JobStatus]

class ErrorClass(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ERROR_CLASS_UNSPECIFIED: _ClassVar[ErrorClass]
    ERROR_CLASS_TRANSIENT: _ClassVar[ErrorClass]
    ERROR_CLASS_RATE_LIMITED: _ClassVar[ErrorClass]
    ERROR_CLASS_AUTH_EXPIRED: _ClassVar[ErrorClass]
    ERROR_CLASS_AUTH_INVALID: _ClassVar[ErrorClass]
    ERROR_CLASS_NOT_FOUND: _ClassVar[ErrorClass]
    ERROR_CLASS_INVALID_INPUT: _ClassVar[ErrorClass]
    ERROR_CLASS_PROVIDER_DOWN: _ClassVar[ErrorClass]
    ERROR_CLASS_WORKER_BUG: _ClassVar[ErrorClass]

class WebhookEventType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WEBHOOK_EVENT_TYPE_UNSPECIFIED: _ClassVar[WebhookEventType]
    WEBHOOK_EVENT_TYPE_ACTIVITY_CREATED: _ClassVar[WebhookEventType]
    WEBHOOK_EVENT_TYPE_ACTIVITY_UPDATED: _ClassVar[WebhookEventType]
    WEBHOOK_EVENT_TYPE_ACTIVITY_DELETED: _ClassVar[WebhookEventType]
    WEBHOOK_EVENT_TYPE_ACCOUNT_DEAUTHORIZED: _ClassVar[WebhookEventType]
WORKER_EVENT_TYPE_UNSPECIFIED: WorkerEventType
WORKER_EVENT_TYPE_ACTIVITY: WorkerEventType
WORKER_EVENT_TYPE_SEGMENT: WorkerEventType
WORKER_EVENT_TYPE_SEGMENT_EFFORT: WorkerEventType
WORKER_EVENT_TYPE_RECORD: WorkerEventType
WORKER_EVENT_TYPE_METRIC: WorkerEventType
WORKER_EVENT_TYPE_GEAR: WorkerEventType
AUTH_METHOD_UNSPECIFIED: AuthMethod
AUTH_METHOD_NONE: AuthMethod
AUTH_METHOD_OAUTH2: AuthMethod
AUTH_METHOD_API_KEY: AuthMethod
AUTH_METHOD_BASIC: AuthMethod
AUTH_METHOD_CUSTOM: AuthMethod
FIELD_TYPE_UNSPECIFIED: FieldType
FIELD_TYPE_TEXT: FieldType
FIELD_TYPE_SECRET: FieldType
FIELD_TYPE_URL: FieldType
FIELD_TYPE_NUMBER: FieldType
FIELD_TYPE_BOOL: FieldType
FIELD_TYPE_SELECT: FieldType
FIELD_TYPE_MULTI_SELECT: FieldType
FIELD_TYPE_DATE: FieldType
JOB_TYPE_UNSPECIFIED: JobType
JOB_TYPE_IMPORT_ACTIVITIES: JobType
JOB_TYPE_REIMPORT_ACTIVITY: JobType
JOB_TYPE_LOCAL_REPARSE: JobType
JOB_TYPE_IMPORT_SEGMENTS: JobType
JOB_TYPE_FETCH_SEGMENT_DETAIL: JobType
JOB_TYPE_IMPORT_METRICS: JobType
JOB_TYPE_REGISTER_WEBHOOK: JobType
JOB_TYPE_UNREGISTER_WEBHOOK: JobType
JOB_TYPE_VALIDATE_CREDENTIALS: JobType
JOB_TYPE_REFRESH_OAUTH_TOKEN: JobType
JOB_TYPE_IMPORT_GEAR: JobType
REPORT_INSTRUCTION_UNSPECIFIED: ReportInstruction
REPORT_INSTRUCTION_NONE: ReportInstruction
REPORT_INSTRUCTION_ACK: ReportInstruction
REPORT_INSTRUCTION_PAUSE_PROVIDER: ReportInstruction
JOB_STATUS_UNSPECIFIED: JobStatus
JOB_STATUS_OK: JobStatus
JOB_STATUS_FAILED: JobStatus
JOB_STATUS_RATE_LIMITED: JobStatus
JOB_STATUS_AUTH_EXPIRED: JobStatus
JOB_STATUS_RETRYABLE: JobStatus
JOB_STATUS_PROVIDER_DOWN: JobStatus
ERROR_CLASS_UNSPECIFIED: ErrorClass
ERROR_CLASS_TRANSIENT: ErrorClass
ERROR_CLASS_RATE_LIMITED: ErrorClass
ERROR_CLASS_AUTH_EXPIRED: ErrorClass
ERROR_CLASS_AUTH_INVALID: ErrorClass
ERROR_CLASS_NOT_FOUND: ErrorClass
ERROR_CLASS_INVALID_INPUT: ErrorClass
ERROR_CLASS_PROVIDER_DOWN: ErrorClass
ERROR_CLASS_WORKER_BUG: ErrorClass
WEBHOOK_EVENT_TYPE_UNSPECIFIED: WebhookEventType
WEBHOOK_EVENT_TYPE_ACTIVITY_CREATED: WebhookEventType
WEBHOOK_EVENT_TYPE_ACTIVITY_UPDATED: WebhookEventType
WEBHOOK_EVENT_TYPE_ACTIVITY_DELETED: WebhookEventType
WEBHOOK_EVENT_TYPE_ACCOUNT_DEAUTHORIZED: WebhookEventType

class RegisterRequest(_message.Message):
    __slots__ = ("auth_token", "manifest", "callback_address")
    AUTH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    MANIFEST_FIELD_NUMBER: _ClassVar[int]
    CALLBACK_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    auth_token: str
    manifest: WorkerManifest
    callback_address: str
    def __init__(self, auth_token: _Optional[str] = ..., manifest: _Optional[_Union[WorkerManifest, _Mapping]] = ..., callback_address: _Optional[str] = ...) -> None: ...

class RegisterResponse(_message.Message):
    __slots__ = ("worker_id", "heartbeat_interval_seconds", "recommended_capacity")
    WORKER_ID_FIELD_NUMBER: _ClassVar[int]
    HEARTBEAT_INTERVAL_SECONDS_FIELD_NUMBER: _ClassVar[int]
    RECOMMENDED_CAPACITY_FIELD_NUMBER: _ClassVar[int]
    worker_id: str
    heartbeat_interval_seconds: int
    recommended_capacity: int
    def __init__(self, worker_id: _Optional[str] = ..., heartbeat_interval_seconds: _Optional[int] = ..., recommended_capacity: _Optional[int] = ...) -> None: ...

class WorkerManifest(_message.Message):
    __slots__ = ("worker_name", "version", "manifest_hash", "providers", "sdk_name", "sdk_version")
    WORKER_NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    MANIFEST_HASH_FIELD_NUMBER: _ClassVar[int]
    PROVIDERS_FIELD_NUMBER: _ClassVar[int]
    SDK_NAME_FIELD_NUMBER: _ClassVar[int]
    SDK_VERSION_FIELD_NUMBER: _ClassVar[int]
    worker_name: str
    version: str
    manifest_hash: str
    providers: _containers.RepeatedCompositeFieldContainer[ProviderManifest]
    sdk_name: str
    sdk_version: str
    def __init__(self, worker_name: _Optional[str] = ..., version: _Optional[str] = ..., manifest_hash: _Optional[str] = ..., providers: _Optional[_Iterable[_Union[ProviderManifest, _Mapping]]] = ..., sdk_name: _Optional[str] = ..., sdk_version: _Optional[str] = ...) -> None: ...

class ProviderManifest(_message.Message):
    __slots__ = ("provider_id", "display_name", "description", "icon_url", "setup_docs_url", "config_fields", "auth_method", "oauth", "supported_jobs", "default_poll_schedule", "supports_webhooks", "supports_backfill", "supports_local_reparse", "producible_events", "capabilities")
    class CapabilitiesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: DataTypeCapability
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[DataTypeCapability, _Mapping]] = ...) -> None: ...
    PROVIDER_ID_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ICON_URL_FIELD_NUMBER: _ClassVar[int]
    SETUP_DOCS_URL_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELDS_FIELD_NUMBER: _ClassVar[int]
    AUTH_METHOD_FIELD_NUMBER: _ClassVar[int]
    OAUTH_FIELD_NUMBER: _ClassVar[int]
    SUPPORTED_JOBS_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_POLL_SCHEDULE_FIELD_NUMBER: _ClassVar[int]
    SUPPORTS_WEBHOOKS_FIELD_NUMBER: _ClassVar[int]
    SUPPORTS_BACKFILL_FIELD_NUMBER: _ClassVar[int]
    SUPPORTS_LOCAL_REPARSE_FIELD_NUMBER: _ClassVar[int]
    PRODUCIBLE_EVENTS_FIELD_NUMBER: _ClassVar[int]
    CAPABILITIES_FIELD_NUMBER: _ClassVar[int]
    provider_id: str
    display_name: str
    description: str
    icon_url: str
    setup_docs_url: str
    config_fields: _containers.RepeatedCompositeFieldContainer[ConfigField]
    auth_method: AuthMethod
    oauth: OAuthConfig
    supported_jobs: _containers.RepeatedScalarFieldContainer[JobType]
    default_poll_schedule: str
    supports_webhooks: bool
    supports_backfill: bool
    supports_local_reparse: bool
    producible_events: _containers.RepeatedScalarFieldContainer[WorkerEventType]
    capabilities: _containers.MessageMap[str, DataTypeCapability]
    def __init__(self, provider_id: _Optional[str] = ..., display_name: _Optional[str] = ..., description: _Optional[str] = ..., icon_url: _Optional[str] = ..., setup_docs_url: _Optional[str] = ..., config_fields: _Optional[_Iterable[_Union[ConfigField, _Mapping]]] = ..., auth_method: _Optional[_Union[AuthMethod, str]] = ..., oauth: _Optional[_Union[OAuthConfig, _Mapping]] = ..., supported_jobs: _Optional[_Iterable[_Union[JobType, str]]] = ..., default_poll_schedule: _Optional[str] = ..., supports_webhooks: _Optional[bool] = ..., supports_backfill: _Optional[bool] = ..., supports_local_reparse: _Optional[bool] = ..., producible_events: _Optional[_Iterable[_Union[WorkerEventType, str]]] = ..., capabilities: _Optional[_Mapping[str, DataTypeCapability]] = ...) -> None: ...

class DataTypeCapability(_message.Message):
    __slots__ = ("read", "write", "push", "backfill", "granularity")
    READ_FIELD_NUMBER: _ClassVar[int]
    WRITE_FIELD_NUMBER: _ClassVar[int]
    PUSH_FIELD_NUMBER: _ClassVar[int]
    BACKFILL_FIELD_NUMBER: _ClassVar[int]
    GRANULARITY_FIELD_NUMBER: _ClassVar[int]
    read: bool
    write: bool
    push: bool
    backfill: bool
    granularity: str
    def __init__(self, read: _Optional[bool] = ..., write: _Optional[bool] = ..., push: _Optional[bool] = ..., backfill: _Optional[bool] = ..., granularity: _Optional[str] = ...) -> None: ...

class OAuthConfig(_message.Message):
    __slots__ = ("authorize_url", "token_url", "scopes", "redirect_path", "pkce", "uses_refresh_tokens")
    AUTHORIZE_URL_FIELD_NUMBER: _ClassVar[int]
    TOKEN_URL_FIELD_NUMBER: _ClassVar[int]
    SCOPES_FIELD_NUMBER: _ClassVar[int]
    REDIRECT_PATH_FIELD_NUMBER: _ClassVar[int]
    PKCE_FIELD_NUMBER: _ClassVar[int]
    USES_REFRESH_TOKENS_FIELD_NUMBER: _ClassVar[int]
    authorize_url: str
    token_url: str
    scopes: _containers.RepeatedScalarFieldContainer[str]
    redirect_path: str
    pkce: bool
    uses_refresh_tokens: bool
    def __init__(self, authorize_url: _Optional[str] = ..., token_url: _Optional[str] = ..., scopes: _Optional[_Iterable[str]] = ..., redirect_path: _Optional[str] = ..., pkce: _Optional[bool] = ..., uses_refresh_tokens: _Optional[bool] = ...) -> None: ...

class ConfigField(_message.Message):
    __slots__ = ("key", "label", "help_text", "type", "required", "validation_regex", "options", "computed_by_core", "placeholder", "default_value")
    KEY_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    HELP_TEXT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_FIELD_NUMBER: _ClassVar[int]
    VALIDATION_REGEX_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    COMPUTED_BY_CORE_FIELD_NUMBER: _ClassVar[int]
    PLACEHOLDER_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    label: str
    help_text: str
    type: FieldType
    required: bool
    validation_regex: str
    options: _containers.RepeatedScalarFieldContainer[str]
    computed_by_core: bool
    placeholder: str
    default_value: str
    def __init__(self, key: _Optional[str] = ..., label: _Optional[str] = ..., help_text: _Optional[str] = ..., type: _Optional[_Union[FieldType, str]] = ..., required: _Optional[bool] = ..., validation_regex: _Optional[str] = ..., options: _Optional[_Iterable[str]] = ..., computed_by_core: _Optional[bool] = ..., placeholder: _Optional[str] = ..., default_value: _Optional[str] = ...) -> None: ...

class DeregisterRequest(_message.Message):
    __slots__ = ("worker_id",)
    WORKER_ID_FIELD_NUMBER: _ClassVar[int]
    worker_id: str
    def __init__(self, worker_id: _Optional[str] = ...) -> None: ...

class DeregisterResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class HeartbeatRequest(_message.Message):
    __slots__ = ("worker_id", "health")
    WORKER_ID_FIELD_NUMBER: _ClassVar[int]
    HEALTH_FIELD_NUMBER: _ClassVar[int]
    worker_id: str
    health: WorkerHealth
    def __init__(self, worker_id: _Optional[str] = ..., health: _Optional[_Union[WorkerHealth, _Mapping]] = ...) -> None: ...

class HeartbeatResponse(_message.Message):
    __slots__ = ("should_shutdown",)
    SHOULD_SHUTDOWN_FIELD_NUMBER: _ClassVar[int]
    should_shutdown: bool
    def __init__(self, should_shutdown: _Optional[bool] = ...) -> None: ...

class WorkerHealth(_message.Message):
    __slots__ = ("active_jobs", "available_capacity", "metrics")
    class MetricsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: float
        def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    ACTIVE_JOBS_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_CAPACITY_FIELD_NUMBER: _ClassVar[int]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    active_jobs: int
    available_capacity: int
    metrics: _containers.ScalarMap[str, float]
    def __init__(self, active_jobs: _Optional[int] = ..., available_capacity: _Optional[int] = ..., metrics: _Optional[_Mapping[str, float]] = ...) -> None: ...

class Job(_message.Message):
    __slots__ = ("id", "type", "provider", "user_id", "external_account_id", "credentials", "import_activities", "reimport_activity", "local_reparse", "import_segments", "import_metrics", "register_webhook", "unregister_webhook", "import_gear", "scheduled_at", "deadline", "attempt", "dry_run")
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    IMPORT_ACTIVITIES_FIELD_NUMBER: _ClassVar[int]
    REIMPORT_ACTIVITY_FIELD_NUMBER: _ClassVar[int]
    LOCAL_REPARSE_FIELD_NUMBER: _ClassVar[int]
    IMPORT_SEGMENTS_FIELD_NUMBER: _ClassVar[int]
    IMPORT_METRICS_FIELD_NUMBER: _ClassVar[int]
    REGISTER_WEBHOOK_FIELD_NUMBER: _ClassVar[int]
    UNREGISTER_WEBHOOK_FIELD_NUMBER: _ClassVar[int]
    IMPORT_GEAR_FIELD_NUMBER: _ClassVar[int]
    SCHEDULED_AT_FIELD_NUMBER: _ClassVar[int]
    DEADLINE_FIELD_NUMBER: _ClassVar[int]
    ATTEMPT_FIELD_NUMBER: _ClassVar[int]
    DRY_RUN_FIELD_NUMBER: _ClassVar[int]
    id: str
    type: JobType
    provider: str
    user_id: str
    external_account_id: str
    credentials: EphemeralCredentials
    import_activities: ImportActivitiesPayload
    reimport_activity: ReimportActivityPayload
    local_reparse: LocalReparsePayload
    import_segments: ImportSegmentsPayload
    import_metrics: ImportMetricsPayload
    register_webhook: RegisterWebhookPayload
    unregister_webhook: UnregisterWebhookPayload
    import_gear: ImportGearPayload
    scheduled_at: _timestamp_pb2.Timestamp
    deadline: _timestamp_pb2.Timestamp
    attempt: int
    dry_run: bool
    def __init__(self, id: _Optional[str] = ..., type: _Optional[_Union[JobType, str]] = ..., provider: _Optional[str] = ..., user_id: _Optional[str] = ..., external_account_id: _Optional[str] = ..., credentials: _Optional[_Union[EphemeralCredentials, _Mapping]] = ..., import_activities: _Optional[_Union[ImportActivitiesPayload, _Mapping]] = ..., reimport_activity: _Optional[_Union[ReimportActivityPayload, _Mapping]] = ..., local_reparse: _Optional[_Union[LocalReparsePayload, _Mapping]] = ..., import_segments: _Optional[_Union[ImportSegmentsPayload, _Mapping]] = ..., import_metrics: _Optional[_Union[ImportMetricsPayload, _Mapping]] = ..., register_webhook: _Optional[_Union[RegisterWebhookPayload, _Mapping]] = ..., unregister_webhook: _Optional[_Union[UnregisterWebhookPayload, _Mapping]] = ..., import_gear: _Optional[_Union[ImportGearPayload, _Mapping]] = ..., scheduled_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., deadline: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., attempt: _Optional[int] = ..., dry_run: _Optional[bool] = ...) -> None: ...

class JobAck(_message.Message):
    __slots__ = ("initial_capacity", "received_job_ids", "rejected_job_ids", "capacity_increment")
    INITIAL_CAPACITY_FIELD_NUMBER: _ClassVar[int]
    RECEIVED_JOB_IDS_FIELD_NUMBER: _ClassVar[int]
    REJECTED_JOB_IDS_FIELD_NUMBER: _ClassVar[int]
    CAPACITY_INCREMENT_FIELD_NUMBER: _ClassVar[int]
    initial_capacity: int
    received_job_ids: _containers.RepeatedScalarFieldContainer[str]
    rejected_job_ids: _containers.RepeatedScalarFieldContainer[str]
    capacity_increment: int
    def __init__(self, initial_capacity: _Optional[int] = ..., received_job_ids: _Optional[_Iterable[str]] = ..., rejected_job_ids: _Optional[_Iterable[str]] = ..., capacity_increment: _Optional[int] = ...) -> None: ...

class EphemeralCredentials(_message.Message):
    __slots__ = ("method", "access_token", "refresh_token", "access_token_expires_at", "client_id", "client_secret", "api_key", "username", "password", "custom", "config")
    class CustomEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class ConfigEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    METHOD_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    REFRESH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SECRET_FIELD_NUMBER: _ClassVar[int]
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    method: AuthMethod
    access_token: str
    refresh_token: str
    access_token_expires_at: _timestamp_pb2.Timestamp
    client_id: str
    client_secret: str
    api_key: str
    username: str
    password: str
    custom: _containers.ScalarMap[str, str]
    config: _containers.ScalarMap[str, str]
    def __init__(self, method: _Optional[_Union[AuthMethod, str]] = ..., access_token: _Optional[str] = ..., refresh_token: _Optional[str] = ..., access_token_expires_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., client_id: _Optional[str] = ..., client_secret: _Optional[str] = ..., api_key: _Optional[str] = ..., username: _Optional[str] = ..., password: _Optional[str] = ..., custom: _Optional[_Mapping[str, str]] = ..., config: _Optional[_Mapping[str, str]] = ...) -> None: ...

class ReportRequest(_message.Message):
    __slots__ = ("worker_id", "job_id", "status", "job_result", "validate_credentials", "refresh_oauth_token", "register_webhook", "error", "rate_limit")
    WORKER_ID_FIELD_NUMBER: _ClassVar[int]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    JOB_RESULT_FIELD_NUMBER: _ClassVar[int]
    VALIDATE_CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    REFRESH_OAUTH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    REGISTER_WEBHOOK_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    RATE_LIMIT_FIELD_NUMBER: _ClassVar[int]
    worker_id: str
    job_id: str
    status: JobStatus
    job_result: JobResult
    validate_credentials: ValidateCredentialsResult
    refresh_oauth_token: RefreshOAuthTokenResult
    register_webhook: RegisterWebhookResult
    error: WorkerError
    rate_limit: RateLimitSnapshot
    def __init__(self, worker_id: _Optional[str] = ..., job_id: _Optional[str] = ..., status: _Optional[_Union[JobStatus, str]] = ..., job_result: _Optional[_Union[JobResult, _Mapping]] = ..., validate_credentials: _Optional[_Union[ValidateCredentialsResult, _Mapping]] = ..., refresh_oauth_token: _Optional[_Union[RefreshOAuthTokenResult, _Mapping]] = ..., register_webhook: _Optional[_Union[RegisterWebhookResult, _Mapping]] = ..., error: _Optional[_Union[WorkerError, _Mapping]] = ..., rate_limit: _Optional[_Union[RateLimitSnapshot, _Mapping]] = ...) -> None: ...

class ReportResponse(_message.Message):
    __slots__ = ("instruction",)
    INSTRUCTION_FIELD_NUMBER: _ClassVar[int]
    instruction: ReportInstruction
    def __init__(self, instruction: _Optional[_Union[ReportInstruction, str]] = ...) -> None: ...

class WorkerError(_message.Message):
    __slots__ = ("code", "message", "retry_after", "metadata")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    CLASS_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    RETRY_AFTER_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    code: str
    message: str
    retry_after: _timestamp_pb2.Timestamp
    metadata: _containers.ScalarMap[str, str]
    def __init__(self, code: _Optional[str] = ..., message: _Optional[str] = ..., retry_after: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., metadata: _Optional[_Mapping[str, str]] = ..., **kwargs) -> None: ...

class RateLimitSnapshot(_message.Message):
    __slots__ = ("short_remaining", "short_limit", "short_reset_at", "long_remaining", "long_limit", "long_reset_at")
    SHORT_REMAINING_FIELD_NUMBER: _ClassVar[int]
    SHORT_LIMIT_FIELD_NUMBER: _ClassVar[int]
    SHORT_RESET_AT_FIELD_NUMBER: _ClassVar[int]
    LONG_REMAINING_FIELD_NUMBER: _ClassVar[int]
    LONG_LIMIT_FIELD_NUMBER: _ClassVar[int]
    LONG_RESET_AT_FIELD_NUMBER: _ClassVar[int]
    short_remaining: int
    short_limit: int
    short_reset_at: _timestamp_pb2.Timestamp
    long_remaining: int
    long_limit: int
    long_reset_at: _timestamp_pb2.Timestamp
    def __init__(self, short_remaining: _Optional[int] = ..., short_limit: _Optional[int] = ..., short_reset_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., long_remaining: _Optional[int] = ..., long_limit: _Optional[int] = ..., long_reset_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class RefreshCredentialsRequest(_message.Message):
    __slots__ = ("worker_id", "external_account_id", "failing_job_id")
    WORKER_ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    FAILING_JOB_ID_FIELD_NUMBER: _ClassVar[int]
    worker_id: str
    external_account_id: str
    failing_job_id: str
    def __init__(self, worker_id: _Optional[str] = ..., external_account_id: _Optional[str] = ..., failing_job_id: _Optional[str] = ...) -> None: ...

class RefreshCredentialsResponse(_message.Message):
    __slots__ = ("credentials",)
    CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    credentials: EphemeralCredentials
    def __init__(self, credentials: _Optional[_Union[EphemeralCredentials, _Mapping]] = ...) -> None: ...

class PresignBlobUploadRequest(_message.Message):
    __slots__ = ("worker_id", "user_id", "external_account_id", "kind", "extension", "content_type", "size_hint_bytes")
    WORKER_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    EXTENSION_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    SIZE_HINT_BYTES_FIELD_NUMBER: _ClassVar[int]
    worker_id: str
    user_id: str
    external_account_id: str
    kind: str
    extension: str
    content_type: str
    size_hint_bytes: int
    def __init__(self, worker_id: _Optional[str] = ..., user_id: _Optional[str] = ..., external_account_id: _Optional[str] = ..., kind: _Optional[str] = ..., extension: _Optional[str] = ..., content_type: _Optional[str] = ..., size_hint_bytes: _Optional[int] = ...) -> None: ...

class PresignBlobUploadResponse(_message.Message):
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

class PresignBlobDownloadRequest(_message.Message):
    __slots__ = ("worker_id", "blob_id")
    WORKER_ID_FIELD_NUMBER: _ClassVar[int]
    BLOB_ID_FIELD_NUMBER: _ClassVar[int]
    worker_id: str
    blob_id: str
    def __init__(self, worker_id: _Optional[str] = ..., blob_id: _Optional[str] = ...) -> None: ...

class PresignBlobDownloadResponse(_message.Message):
    __slots__ = ("download_url", "expires_at", "content_type", "size_bytes")
    DOWNLOAD_URL_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    download_url: str
    expires_at: _timestamp_pb2.Timestamp
    content_type: str
    size_bytes: int
    def __init__(self, download_url: _Optional[str] = ..., expires_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., content_type: _Optional[str] = ..., size_bytes: _Optional[int] = ...) -> None: ...

class ImportActivitiesPayload(_message.Message):
    __slots__ = ("since", "until", "max_count")
    SINCE_FIELD_NUMBER: _ClassVar[int]
    UNTIL_FIELD_NUMBER: _ClassVar[int]
    MAX_COUNT_FIELD_NUMBER: _ClassVar[int]
    since: _timestamp_pb2.Timestamp
    until: _timestamp_pb2.Timestamp
    max_count: int
    def __init__(self, since: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., until: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., max_count: _Optional[int] = ...) -> None: ...

class ReimportActivityPayload(_message.Message):
    __slots__ = ("external_id", "activity_source_id")
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    external_id: str
    activity_source_id: str
    def __init__(self, external_id: _Optional[str] = ..., activity_source_id: _Optional[str] = ...) -> None: ...

class LocalReparsePayload(_message.Message):
    __slots__ = ("activity_source_id", "raw_blob_id")
    ACTIVITY_SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    RAW_BLOB_ID_FIELD_NUMBER: _ClassVar[int]
    activity_source_id: str
    raw_blob_id: str
    def __init__(self, activity_source_id: _Optional[str] = ..., raw_blob_id: _Optional[str] = ...) -> None: ...

class ImportSegmentsPayload(_message.Message):
    __slots__ = ("since",)
    SINCE_FIELD_NUMBER: _ClassVar[int]
    since: _timestamp_pb2.Timestamp
    def __init__(self, since: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ImportMetricsPayload(_message.Message):
    __slots__ = ("since", "metric_keys")
    SINCE_FIELD_NUMBER: _ClassVar[int]
    METRIC_KEYS_FIELD_NUMBER: _ClassVar[int]
    since: _timestamp_pb2.Timestamp
    metric_keys: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, since: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., metric_keys: _Optional[_Iterable[str]] = ...) -> None: ...

class ImportGearPayload(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ExternalRef(_message.Message):
    __slots__ = ("user_id", "provider", "external_account_id", "external_id")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    provider: str
    external_account_id: str
    external_id: str
    def __init__(self, user_id: _Optional[str] = ..., provider: _Optional[str] = ..., external_account_id: _Optional[str] = ..., external_id: _Optional[str] = ...) -> None: ...

class JobResult(_message.Message):
    __slots__ = ("events", "new_watermark", "more_available", "worker_name", "worker_version", "worker_package", "payload_ref", "worker_release", "error", "failed_ref")
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    NEW_WATERMARK_FIELD_NUMBER: _ClassVar[int]
    MORE_AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    WORKER_NAME_FIELD_NUMBER: _ClassVar[int]
    WORKER_VERSION_FIELD_NUMBER: _ClassVar[int]
    WORKER_PACKAGE_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_REF_FIELD_NUMBER: _ClassVar[int]
    WORKER_RELEASE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    FAILED_REF_FIELD_NUMBER: _ClassVar[int]
    events: _containers.RepeatedCompositeFieldContainer[WorkerEvent]
    new_watermark: _timestamp_pb2.Timestamp
    more_available: bool
    worker_name: str
    worker_version: str
    worker_package: str
    payload_ref: PayloadRef
    worker_release: str
    error: WorkerError
    failed_ref: ExternalRef
    def __init__(self, events: _Optional[_Iterable[_Union[WorkerEvent, _Mapping]]] = ..., new_watermark: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., more_available: _Optional[bool] = ..., worker_name: _Optional[str] = ..., worker_version: _Optional[str] = ..., worker_package: _Optional[str] = ..., payload_ref: _Optional[_Union[PayloadRef, _Mapping]] = ..., worker_release: _Optional[str] = ..., error: _Optional[_Union[WorkerError, _Mapping]] = ..., failed_ref: _Optional[_Union[ExternalRef, _Mapping]] = ...) -> None: ...

class PayloadRef(_message.Message):
    __slots__ = ("blob_id", "size_bytes", "content_type", "content_sha256")
    BLOB_ID_FIELD_NUMBER: _ClassVar[int]
    SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_SHA256_FIELD_NUMBER: _ClassVar[int]
    blob_id: str
    size_bytes: int
    content_type: str
    content_sha256: str
    def __init__(self, blob_id: _Optional[str] = ..., size_bytes: _Optional[int] = ..., content_type: _Optional[str] = ..., content_sha256: _Optional[str] = ...) -> None: ...

class WorkerEvent(_message.Message):
    __slots__ = ("type", "activity", "segment", "segment_effort", "record", "metric", "gear")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_FIELD_NUMBER: _ClassVar[int]
    SEGMENT_FIELD_NUMBER: _ClassVar[int]
    SEGMENT_EFFORT_FIELD_NUMBER: _ClassVar[int]
    RECORD_FIELD_NUMBER: _ClassVar[int]
    METRIC_FIELD_NUMBER: _ClassVar[int]
    GEAR_FIELD_NUMBER: _ClassVar[int]
    type: WorkerEventType
    activity: ImportedActivity
    segment: ImportedSegment
    segment_effort: ImportedSegmentEffort
    record: ImportedRecord
    metric: ImportedMetric
    gear: ImportedGear
    def __init__(self, type: _Optional[_Union[WorkerEventType, str]] = ..., activity: _Optional[_Union[ImportedActivity, _Mapping]] = ..., segment: _Optional[_Union[ImportedSegment, _Mapping]] = ..., segment_effort: _Optional[_Union[ImportedSegmentEffort, _Mapping]] = ..., record: _Optional[_Union[ImportedRecord, _Mapping]] = ..., metric: _Optional[_Union[ImportedMetric, _Mapping]] = ..., gear: _Optional[_Union[ImportedGear, _Mapping]] = ...) -> None: ...

class ImportedActivity(_message.Message):
    __slots__ = ("ref", "raw_blob_id", "payload", "stream", "attachments", "raw_content_type", "raw_size_bytes")
    REF_FIELD_NUMBER: _ClassVar[int]
    RAW_BLOB_ID_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    STREAM_FIELD_NUMBER: _ClassVar[int]
    ATTACHMENTS_FIELD_NUMBER: _ClassVar[int]
    RAW_CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    RAW_SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    ref: ExternalRef
    raw_blob_id: str
    payload: _activity_pb2.ActivitySourcePayload
    stream: _activity_pb2.ActivityStream
    attachments: _containers.RepeatedCompositeFieldContainer[Attachment]
    raw_content_type: str
    raw_size_bytes: int
    def __init__(self, ref: _Optional[_Union[ExternalRef, _Mapping]] = ..., raw_blob_id: _Optional[str] = ..., payload: _Optional[_Union[_activity_pb2.ActivitySourcePayload, _Mapping]] = ..., stream: _Optional[_Union[_activity_pb2.ActivityStream, _Mapping]] = ..., attachments: _Optional[_Iterable[_Union[Attachment, _Mapping]]] = ..., raw_content_type: _Optional[str] = ..., raw_size_bytes: _Optional[int] = ...) -> None: ...

class Attachment(_message.Message):
    __slots__ = ("blob_id", "external_url", "content_type", "caption", "width", "height")
    BLOB_ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_URL_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    CAPTION_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    blob_id: str
    external_url: str
    content_type: str
    caption: str
    width: int
    height: int
    def __init__(self, blob_id: _Optional[str] = ..., external_url: _Optional[str] = ..., content_type: _Optional[str] = ..., caption: _Optional[str] = ..., width: _Optional[int] = ..., height: _Optional[int] = ...) -> None: ...

class ImportedSegment(_message.Message):
    __slots__ = ("ref", "payload")
    REF_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    ref: ExternalRef
    payload: SegmentImport
    def __init__(self, ref: _Optional[_Union[ExternalRef, _Mapping]] = ..., payload: _Optional[_Union[SegmentImport, _Mapping]] = ...) -> None: ...

class SegmentImport(_message.Message):
    __slots__ = ("name", "description", "activity_type", "encoded_polyline", "distance_m", "elevation_gain_m", "elevation_loss_m", "avg_grade", "max_grade", "climb_category", "bidirectional", "starred")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_TYPE_FIELD_NUMBER: _ClassVar[int]
    ENCODED_POLYLINE_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_M_FIELD_NUMBER: _ClassVar[int]
    ELEVATION_GAIN_M_FIELD_NUMBER: _ClassVar[int]
    ELEVATION_LOSS_M_FIELD_NUMBER: _ClassVar[int]
    AVG_GRADE_FIELD_NUMBER: _ClassVar[int]
    MAX_GRADE_FIELD_NUMBER: _ClassVar[int]
    CLIMB_CATEGORY_FIELD_NUMBER: _ClassVar[int]
    BIDIRECTIONAL_FIELD_NUMBER: _ClassVar[int]
    STARRED_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    activity_type: _activity_pb2.ActivityType
    encoded_polyline: str
    distance_m: float
    elevation_gain_m: float
    elevation_loss_m: float
    avg_grade: float
    max_grade: float
    climb_category: _segment_pb2.ClimbCategory
    bidirectional: bool
    starred: bool
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., activity_type: _Optional[_Union[_activity_pb2.ActivityType, str]] = ..., encoded_polyline: _Optional[str] = ..., distance_m: _Optional[float] = ..., elevation_gain_m: _Optional[float] = ..., elevation_loss_m: _Optional[float] = ..., avg_grade: _Optional[float] = ..., max_grade: _Optional[float] = ..., climb_category: _Optional[_Union[_segment_pb2.ClimbCategory, str]] = ..., bidirectional: _Optional[bool] = ..., starred: _Optional[bool] = ...) -> None: ...

class ImportedSegmentEffort(_message.Message):
    __slots__ = ("ref", "activity_external_id", "segment_external_id", "payload")
    REF_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    SEGMENT_EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    ref: ExternalRef
    activity_external_id: str
    segment_external_id: str
    payload: SegmentEffortImport
    def __init__(self, ref: _Optional[_Union[ExternalRef, _Mapping]] = ..., activity_external_id: _Optional[str] = ..., segment_external_id: _Optional[str] = ..., payload: _Optional[_Union[SegmentEffortImport, _Mapping]] = ...) -> None: ...

class SegmentEffortImport(_message.Message):
    __slots__ = ("start_time", "elapsed", "moving", "start_offset", "end_offset", "avg_heart_rate_bpm", "max_heart_rate_bpm", "avg_power_w", "avg_cadence", "avg_speed_mps")
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    ELAPSED_FIELD_NUMBER: _ClassVar[int]
    MOVING_FIELD_NUMBER: _ClassVar[int]
    START_OFFSET_FIELD_NUMBER: _ClassVar[int]
    END_OFFSET_FIELD_NUMBER: _ClassVar[int]
    AVG_HEART_RATE_BPM_FIELD_NUMBER: _ClassVar[int]
    MAX_HEART_RATE_BPM_FIELD_NUMBER: _ClassVar[int]
    AVG_POWER_W_FIELD_NUMBER: _ClassVar[int]
    AVG_CADENCE_FIELD_NUMBER: _ClassVar[int]
    AVG_SPEED_MPS_FIELD_NUMBER: _ClassVar[int]
    start_time: _timestamp_pb2.Timestamp
    elapsed: _duration_pb2.Duration
    moving: _duration_pb2.Duration
    start_offset: int
    end_offset: int
    avg_heart_rate_bpm: int
    max_heart_rate_bpm: int
    avg_power_w: int
    avg_cadence: int
    avg_speed_mps: float
    def __init__(self, start_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., elapsed: _Optional[_Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]] = ..., moving: _Optional[_Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]] = ..., start_offset: _Optional[int] = ..., end_offset: _Optional[int] = ..., avg_heart_rate_bpm: _Optional[int] = ..., max_heart_rate_bpm: _Optional[int] = ..., avg_power_w: _Optional[int] = ..., avg_cadence: _Optional[int] = ..., avg_speed_mps: _Optional[float] = ...) -> None: ...

class ImportedRecord(_message.Message):
    __slots__ = ("ref", "activity_external_id", "payload")
    REF_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    ref: ExternalRef
    activity_external_id: str
    payload: RecordImport
    def __init__(self, ref: _Optional[_Union[ExternalRef, _Mapping]] = ..., activity_external_id: _Optional[str] = ..., payload: _Optional[_Union[RecordImport, _Mapping]] = ...) -> None: ...

class RecordImport(_message.Message):
    __slots__ = ("metric", "duration", "distance_m", "value", "start_offset")
    METRIC_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_M_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    START_OFFSET_FIELD_NUMBER: _ClassVar[int]
    metric: _activity_pb2.BestEffortMetric
    duration: _duration_pb2.Duration
    distance_m: float
    value: float
    start_offset: int
    def __init__(self, metric: _Optional[_Union[_activity_pb2.BestEffortMetric, str]] = ..., duration: _Optional[_Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]] = ..., distance_m: _Optional[float] = ..., value: _Optional[float] = ..., start_offset: _Optional[int] = ...) -> None: ...

class ImportedMetric(_message.Message):
    __slots__ = ("ref", "key", "ts", "value_numeric", "value_json")
    REF_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    TS_FIELD_NUMBER: _ClassVar[int]
    VALUE_NUMERIC_FIELD_NUMBER: _ClassVar[int]
    VALUE_JSON_FIELD_NUMBER: _ClassVar[int]
    ref: ExternalRef
    key: str
    ts: _timestamp_pb2.Timestamp
    value_numeric: float
    value_json: str
    def __init__(self, ref: _Optional[_Union[ExternalRef, _Mapping]] = ..., key: _Optional[str] = ..., ts: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., value_numeric: _Optional[float] = ..., value_json: _Optional[str] = ...) -> None: ...

class ImportedGear(_message.Message):
    __slots__ = ("ref", "payload")
    REF_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    ref: ExternalRef
    payload: GearImport
    def __init__(self, ref: _Optional[_Union[ExternalRef, _Mapping]] = ..., payload: _Optional[_Union[GearImport, _Mapping]] = ...) -> None: ...

class GearImport(_message.Message):
    __slots__ = ("kind", "name", "brand", "model", "description", "retired", "primary", "distance_m", "default_for")
    KIND_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    BRAND_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    RETIRED_FIELD_NUMBER: _ClassVar[int]
    PRIMARY_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_M_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_FOR_FIELD_NUMBER: _ClassVar[int]
    kind: _gear_pb2.GearKind
    name: str
    brand: str
    model: str
    description: str
    retired: bool
    primary: bool
    distance_m: float
    default_for: _containers.RepeatedScalarFieldContainer[_activity_pb2.ActivityType]
    def __init__(self, kind: _Optional[_Union[_gear_pb2.GearKind, str]] = ..., name: _Optional[str] = ..., brand: _Optional[str] = ..., model: _Optional[str] = ..., description: _Optional[str] = ..., retired: _Optional[bool] = ..., primary: _Optional[bool] = ..., distance_m: _Optional[float] = ..., default_for: _Optional[_Iterable[_Union[_activity_pb2.ActivityType, str]]] = ...) -> None: ...

class RegisterWebhookPayload(_message.Message):
    __slots__ = ("callback_url", "event_types")
    CALLBACK_URL_FIELD_NUMBER: _ClassVar[int]
    EVENT_TYPES_FIELD_NUMBER: _ClassVar[int]
    callback_url: str
    event_types: _containers.RepeatedScalarFieldContainer[WebhookEventType]
    def __init__(self, callback_url: _Optional[str] = ..., event_types: _Optional[_Iterable[_Union[WebhookEventType, str]]] = ...) -> None: ...

class RegisterWebhookResult(_message.Message):
    __slots__ = ("subscription_id",)
    SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    subscription_id: str
    def __init__(self, subscription_id: _Optional[str] = ...) -> None: ...

class UnregisterWebhookPayload(_message.Message):
    __slots__ = ("subscription_id",)
    SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    subscription_id: str
    def __init__(self, subscription_id: _Optional[str] = ...) -> None: ...

class ValidateCredentialsResult(_message.Message):
    __slots__ = ("valid", "access_token_expires_at")
    VALID_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    valid: bool
    access_token_expires_at: _timestamp_pb2.Timestamp
    def __init__(self, valid: _Optional[bool] = ..., access_token_expires_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class RefreshOAuthTokenResult(_message.Message):
    __slots__ = ("access_token", "refresh_token", "access_token_expires_at")
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    REFRESH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    access_token: str
    refresh_token: str
    access_token_expires_at: _timestamp_pb2.Timestamp
    def __init__(self, access_token: _Optional[str] = ..., refresh_token: _Optional[str] = ..., access_token_expires_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
