# Cairn Garmin worker (Python)

Imports Garmin Connect activities and daily health metrics (HRV, sleep,
weight, steps, resting HR) into Cairn. Garmin has no public activity OAuth
API, so this uses the [`garminconnect`](https://pypi.org/project/garminconnect/)
library (Garth SSO with email/password).

It speaks Cairn's NATS control plane: serves `cairn.discover.garmin`, pulls
jobs from `cairn.jobs.*.garmin`, publishes protojson `cairn.worker.v1.JobResult`
to `cairn.results.*.garmin`, and heartbeats its capability manifest to the
`cairn_worker_presence` KV.

This is a **standalone repository** with no dependency on cairn-core. The only
contract it shares with the server is the proto messages (committed under
`proto/`) and the NATS subjects. Regenerate + recommit `proto/` from the Cairn
proto contract when it changes.

## Run (dev)

Dependencies are managed with [uv](https://docs.astral.sh/uv/) (`pyproject.toml`
+ `uv.lock`; Python version in `.python-version`).

```bash
uv sync --locked
export CAIRN_NATS_URL=nats://localhost:4222
export CAIRN_GARMIN_EMAIL=you@example.com   # dev fallback; prod creds come from the server
export CAIRN_GARMIN_PASSWORD=...
uv run python -m cairn_garmin.main
```

The generated proto stubs are loaded from `./proto` (override with
`CAIRN_PROTO_PATH`). `make check` runs lint, mypy strict, the tests with a
coverage floor, the dependency audit, the image build and fleetlint; see
[CONTRIBUTING.md](CONTRIBUTING.md) and [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

### MFA accounts

The worker cannot answer an MFA prompt. Seed the Garth token store once with an
interactive login, then point the worker at it. Tokens live under
`$CAIRN_GARTH_HOME/<account_id>`, where `<account_id>` is the `account_id` the
server puts in that connection's jobs (`default` for the env-var dev fallback):

```bash
export CAIRN_GARMIN_EMAIL=you@example.com CAIRN_GARMIN_PASSWORD=...
uv run python -c "import os; from garminconnect import Garmin; g = Garmin(os.environ['CAIRN_GARMIN_EMAIL'], os.environ['CAIRN_GARMIN_PASSWORD'], prompt_mfa=lambda: input('MFA code: ')); g.login(); g.client.dump('/data/garth/<account_id>')"
```

The command prompts `MFA code:` on the terminal. Mount the resulting directory
into the container (the image sets `CAIRN_GARTH_HOME=/data/garth` and declares
`/data` as a volume); the worker resumes from the cached tokens and refreshes
them itself.

The image runs as the unprivileged user `cairn` (uid/gid 10001), so the token
directory must be readable and writable by that uid (`chown -R 10001:10001`, or
`fsGroup: 10001` in Kubernetes).

## Configuration

All settings are read from the environment in `cairn_garmin/config.py`.

| Variable | Default | Purpose |
| --- | --- | --- |
| `CAIRN_NATS_URL` | `nats://localhost:4222` | NATS server. |
| `CAIRN_WORKER_ENROLLMENT_TOKEN` | empty | Enrollment token from cairn-core; sent as the NATS CONNECT token. Takes precedence over user/password. See [NATS auth](#nats-auth). |
| `CAIRN_NATS_USER` / `CAIRN_NATS_PASSWORD` | empty (anonymous) | Static NATS user/password auth, used when no enrollment token is set. |
| `CAIRN_WORKER_NAME` | `garmin-fetcher` | Routing identity; must match the server-side enrollment name. Shared by all replicas. |
| `CAIRN_WORKER_INSTANCE_ID` | random 12-hex id | Per-replica presence key. Set to the pod name so a restart reuses its key. |
| `CAIRN_HEARTBEAT_INTERVAL_S` | `20` | Presence heartbeat interval. |
| `CAIRN_PULL_BATCH` | `4` | Jobs fetched per pull. |
| `CAIRN_GARMIN_EMAIL` / `CAIRN_GARMIN_PASSWORD` | empty | Dev fallback credentials, used only when a job carries no account. |
| `CAIRN_GARTH_HOME` | `~/.cache/cairn-garth` (`/data/garth` in the image) | Garth token store root; one subdirectory per account. |
| `CAIRN_GARMIN_FETCH_ACTIVITY_GEAR` | `true` | Look up the gear recorded on each fetched activity (one extra call per activity). |
| `CAIRN_PROTO_PATH` | `./proto` | Location of the generated proto stubs. |

Provider name (`garmin`), package and parser version are baked into
`config.py` and are not overridable; they define the worker's contract (see
[Versioning](#versioning)).

### NATS auth

The worker connects in one of three ways, in this order of precedence:

1. **Enrollment token** (`CAIRN_WORKER_ENROLLMENT_TOKEN`, recommended). Create
   an enrollment in cairn-core (`POST /api/admin/worker-enrollments`, provider
   `garmin`, name = `CAIRN_WORKER_NAME`). The worker presents only the token
   on CONNECT, with the connection name set to `CAIRN_WORKER_NAME`; no client
   nkey is used. nats-server hands the connection to core's auth-callout, which
   validates the enrollment and returns a user JWT limited to core's worker
   permission template for `garmin`. Needs cairn-core 0.3.1 or later with the
   auth-callout enabled (`CAIRN_NATS_AUTH_CALLOUT=true`,
   `CAIRN_NATS_WORKER_ACCOUNT`; see core's `docker/nats-auth-callout.conf`).
   If user/password is also set, it is ignored with a warning.
2. **User/password** (`CAIRN_NATS_USER` / `CAIRN_NATS_PASSWORD`): a static
   nats.conf user, e.g. for a server without the auth-callout. Its permissions
   must grant the worker permission template's subjects for `garmin`.
3. **Anonymous**, for a dev server without auth.

`tests/test_nats_permissions.py` runs the worker's NATS operations against a
real nats-server both ways: as a static user carrying the template, and through
the auth-callout flow with a test responder that issues the user JWT the way
core does.

## Versioning

Three versions, defined in [core ADR 0005](https://github.com/opencairn-org/cairn-core/blob/main/docs/adr/0005-provider-versioning.md)
and the [provider contract](https://docs.opencairn.org/architecture/provider-contract#versioning):

- **Release** (`vX.Y.Z`, the git tag): major.minor must match core.
- **Dataset** (`N`, the archive envelope `version`): bump only when the parser
  can no longer read the previous archive format.
- **Parser** (`N.M`, sent as `worker_version`): bump `M` with **every** change
  to the parsed output; a dataset bump resets it to `N.0`. Parser `N.x` must
  read every dataset `N` archive. Versions only move forward.
  `tests/test_parser_golden.py` pins the parsed output of `tests/data/archives`
  per parser version; after a bump, `CAIRN_UPDATE_GOLDEN=1 make test` writes
  the new goldens (delete the old ones). The archive envelope holds every
  parser input (activity, details, per-activity gear), and import and re-parse
  run the same `mapping.parse_archive`.

Jobs are routed per pool (core ADR 0006): this worker consumes
`cairn.jobs.<job>.garmin.<CAIRN_WORKER_NAME>`. Instances sharing a name share
the work; a second name is a separate pool that core assigns accounts to.

## What it does

Handlers in `cairn_garmin/runtime.py`:

- `discover` (request/reply on `cairn.discover.garmin`): paged activity listing
  for the server's Sync / Full-Sync.
- `fetch_source`: imports one activity (summary, and the sample stream when
  `fetch_streams` is set) and archives the raw response to the blob store.
- `reconcile`: lists activity since the watermark (bounded to 30 days), enqueues
  `fetch_source` for unknown activities, and publishes the new watermark to
  `cairn.results.reconcile.garmin.<account_id>`. Backlog jobs for the same
  account are coalesced within 10 minutes.
- `import_metrics`: daily HRV / Sleep / Weight / Steps / RestingHR as
  `ImportedMetric` events (the server persists them to `health_samples`).
  Trigger from the Connections UI ("Import health").
- `parse_blob`: re-maps an archived raw response with the current mapping
  logic, without calling Garmin.
- `import_gear`: the account's gear list (bikes, shoes), retired included,
  with Garmin's per-activity-type defaults, as `ImportedGear` events. Triggered
  on connect, from the Connections UI ("Sync gear") and with every reconcile.
  `fetch_source` also records the gear used on each activity (one extra
  Garmin call; `CAIRN_GARMIN_FETCH_ACTIVITY_GEAR=false` switches it off).
  Archived responses carry no gear, so already imported activities need a
  reimport, not a reparse, to get it.

Event-carrying results are claim-checked through the blob store; jobs that keep
failing are terminated after five deliveries with a failure envelope carrying
the real error.

Per-user credentials are delivered via `cairn.creds.garmin.get`. The capability
manifest advertises Activity, HRV, Sleep, Weight, Steps, RestingHR and Gear.

Field mapping (activity and health) is verified against a small set of live
activities; see `cairn_garmin/mapping.py` for observed quirks such as
duplicated stream timestamps on Zwift-synced rides.
