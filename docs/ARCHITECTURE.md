# Architecture

cairn-provider-garmin is a Cairn worker: a long-running Python process that
imports Garmin Connect activities and daily health metrics into a Cairn server.
It talks to the server only over NATS and to object storage only through URLs
the server presigns. The handlers and settings are listed in the
[README](../README.md#what-it-does).

## Components

- **`cairn_garmin/main.py`** — entrypoint; wires SIGINT/SIGTERM to a clean stop.
- **`cairn_garmin/runtime.py`** — the `Worker`, a `cairn_provider_sdk.Worker`
  with the Garmin handlers: `discover` and one handler per job kind
  (`fetch_source`, `import_metrics`, `parse_blob`, `reconcile`, `import_gear`).
  The SDK owns the connection, presence, manifest, consumers, retries, ack
  extension, claim-checked results and failure envelopes.
- **`cairn_garmin/garmin_client.py`** — a thin wrapper over `garminconnect`
  with a per-account token store and the pure health-metric extraction.
- **`cairn_garmin/mapping.py`** — pure functions from Garmin JSON to the
  `cairn.worker.v1` / `cairn.v1` proto messages.
- **cairn-provider-sdk** — the runtime, blob I/O through presigned URLs and
  the generated contract stubs (`cairn.v1`, `cairn.worker.v1`).

## Boundaries

- The only contract with the server is the proto messages plus the NATS
  subjects, both from the SDK. There is no code dependency on cairn-core.
- Garmin credentials are never part of a job: the worker requests them per
  account on `cairn.creds.garmin.get` and caches only the resulting client.
- Blob storage is reached only via presigned URLs from the server; the worker
  holds no storage credentials.

## Data flow

1. The server schedules a job on `cairn.jobs.<kind>.garmin` in the `CAIRN_JOBS`
   stream; the worker pulls it with a durable consumer.
2. The handler resolves the account's `GarminClient` (credentials RPC, token
   store under `$CAIRN_GARTH_HOME/<account_id>`) and calls Garmin in a thread.
3. `mapping` turns the responses into `WorkerEvent`s; `fetch_source` also
   archives the raw response for later `parse_blob` re-mapping.
4. The `JobResult` is published to `cairn.results.<kind>.garmin`. Results with
   events are uploaded to the blob store first and only a `payload_ref`
   envelope travels over NATS.
5. A failing job is NAKed with a delay and terminated after five deliveries
   with a failure envelope that carries the real error.

## Decisions

- **NATS pull consumers instead of HTTP callbacks.** Workers scale out by
  adding replicas, need no inbound network access, and JetStream keeps jobs
  durable across restarts.
- **Claim-check for results.** Activity streams can exceed the broker's
  `max_payload`; uploading the body and publishing a reference keeps every
  message small regardless of activity size.
- **The contract comes from the SDK.** The worker pins the contract version
  through the SDK release it is built on and builds without buf or
  cairn-core; the runtime is tested once, in the SDK.
