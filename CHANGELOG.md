# Changelog

All notable changes to the Cairn Garmin worker are documented here. The format
follows [Keep a Changelog](https://keepachangelog.com/), and the project aims
to follow [Semantic Versioning](https://semver.org/). Dates are ISO-8601.

## [Unreleased]

### Added
- A v* tag now also publishes the GitHub release: the tag's CHANGELOG.md
  section as notes plus the image digest and verify commands, with an SPDX
  SBOM of that digest (syft) attached. Before, the release object was created
  by hand (and skipped for 0.5.0).

## [0.5.0] — 2026-10-25

Needs cairn-core 0.5.0 (per-pool subjects and the release check; the Core
must be upgraded first). Upgrade the worker in place: it drains jobs queued
on the 0.4 subjects once. Activities imported before 0.5.0 need a re-fetch to
gain gear: their archives have none.

### Added
- The archive envelope holds every parser input, now including the
  per-activity gear lookup (`null` when not looked up). Import and re-parse
  run the same `mapping.parse_archive`, so a re-parse reproduces the import
  and yields gear for archives that have it.
- Parser version `1.2` (gear from the archive; stable stream channel order)
  on dataset 1; `tests/test_parser_golden.py` pins the output per parser
  version. `parse_blob` refuses archives of another dataset and hands back
  jobs whose `min_parser_version` is newer, backing off for about an hour
  before reporting `parser_too_old`.
- Payloads carry `gear_unknown` when the archive has no gear lookup, so core
  keeps the previous gear on re-import.
- The release is written into the image at build time and sent in presence
  and results; the worker refuses to run against an incompatible core.

### Changed
- Jobs, discovery and results are per pool: `cairn.jobs.<job>.garmin.<name>`,
  `cairn.discover.garmin.<name>`, `cairn.results.<job>.garmin.<name>`.
- Proto stubs regenerated from the cairn-core 0.5.0 contract; `filelock`
  updated for pip-audit.

## [0.4.0] — 2026-10-21

Needs cairn-core 0.4.0 or later (gear events and the `import_gear` job are
new in the contract; the Core must be upgraded first).

### Added
- Gear. The `import_gear` job answers with the account's gear list, retired
  included, with brand, model and Garmin's per-activity-type defaults, as
  GEAR events; `fetch_source` looks up the gear recorded on each activity
  (`get_activity_gear`, one extra call, off with
  `CAIRN_GARMIN_FETCH_ACTIVITY_GEAR=false`) and carries it on the payload,
  preceded by the GEAR event. Already imported activities need a reimport to
  pick up gear. The manifest now declares `Gear` with backfill.

### Changed
- Proto stubs regenerated from the cairn-core 0.4.0 contract.

## [0.3.2] — 2026-10-19

### Added
- `make mutate`: mutmut mutation testing of `cairn_garmin` with a score floor, run weekly in CI.
- `make lint` runs pylint's duplicate-code check (everything else stays with ruff).
- Code of conduct (Contributor Covenant) and an ADR log under `docs/adr`.

### Changed
- The project moved to the `opencairn-org` GitHub organization. The image is
  published as `ghcr.io/opencairn-org/cairn-provider-garmin`; the
  `ghcr.io/johnnycube` namespace keeps the tags published so far as a frozen
  mirror and receives no new versions, so image pins should move.

## [0.3.1] — 2026-10-15

### Added
- Enrollment-token auth: with `CAIRN_WORKER_ENROLLMENT_TOKEN` set, the worker
  presents the token on CONNECT (no client nkey) and is admitted by
  cairn-core's NATS auth-callout, scoped to the `garmin` worker permission
  template. Needs cairn-core 0.3.1 or later with the auth-callout enabled. The
  token takes precedence over `CAIRN_NATS_USER`/`CAIRN_NATS_PASSWORD` (a
  warning is logged if both are set); user/password and anonymous still work.
- The NATS permission integration test also runs through the auth-callout
  flow (nats-server with an `auth_callout` block and no nkey users, plus a
  test responder issuing core-style user JWTs) and checks that a bad token is
  refused.

### Changed
- The NATS connection name is now `CAIRN_WORKER_NAME` (was
  `<name>-garmin`); core's auth-callout matches it against the enrollment
  name.

## [0.3.0] — 2026-10-15

Released alongside Cairn v0.3.0; no worker code changes since 0.2.3.

### Changed
- Under NATS auth (enrolled workers), this worker needs cairn-core 0.3.0 or
  later: earlier worker permission templates refused its job consumers and
  sub-job enqueues.

### Added
- An integration test runs the worker's NATS operations (durable consumers,
  presence KV, discover, credentials, claim-checked results, reconcile
  sub-jobs, acks) against a real nats-server that grants only cairn-core's
  worker permission template, so a subject missing from the template fails
  the build. `make tools` installs the pinned nats-server (`go install`,
  verified against the Go checksum database). Running under NATS auth needs
  cairn-core with the aligned template (cairn-core PR #134).

## [0.2.3] — 2026-10-15

### Fixed
- A stream descriptor without `metricsIndex` no longer crashes the activity
  stream; the descriptor is skipped.

### Changed
- The image runs as the unprivileged user `cairn` (uid/gid 10001) instead of
  root. Only deployments that mount an existing `/data` volume written by the
  old image need to make it writable for that uid; otherwise cached Garmin
  tokens cannot be read.
- Dependencies are locked with uv (`pyproject.toml` + `uv.lock`); the image
  installs exactly the locked set. `requirements*.txt` are gone.
- Base images are pinned by digest; release images get commit-derived
  timestamps (`SOURCE_DATE_EPOCH`).
- The dev-fallback token store defaults to `~/.cache/cairn-garth` instead of
  `/tmp/cairn-garth`.
- The MFA seeding recipe uses garminconnect, since garminconnect 0.3 no longer
  depends on garth.
- `make check` gates CI and releases: ruff, mypy strict, tests with a coverage
  floor, pip-audit, licenses, gitleaks and the image build. CodeQL runs on
  pull requests.

## [0.2.2] — 2026-09-14

### Fixed
- Token persistence after a fresh login. garminconnect 0.3 renamed the
  `garth` client attribute to `client`, so the token dump raised and was
  silently swallowed; every job logged in to Garmin again. The worker now
  resolves either attribute and logs a warning if the write fails.
- Health-metric calls propagate authentication failures (401/403) instead of
  reporting an empty day; other per-metric errors are logged at debug.

### Changed
- README rewritten to match the code: full handler list (discover,
  fetch_source, reconcile, import_metrics, parse_blob), a configuration table
  with the real defaults, and the one-off Garth login recipe for MFA accounts.

### Removed
- The `Lap` capability from the manifest — the worker never emitted lap events.
- The unused `CAIRN_WORKER_ENROLLMENT_TOKEN` setting and the `nkeys`
  dependency; NATS auth is anonymous or user/password.

## [0.2.1] — 2026-09-11

### Changed
- Release images are signed keyless with cosign (Fulcio certificate bound to
  this repository's release workflow) and ship SLSA provenance and SBOM
  attestations; verify with `cosign verify` as documented in the workflow
  header. No functional change to the worker.
- GitHub Actions moved to the current majors of checkout, setup-python, and
  the docker build actions.

### Removed
- The Gitea mirror workflow — the repository is published from GitHub only.

## [0.2.0] — 2026-07-16

**First public release.** A standalone Python worker that imports Garmin
Connect activities and health metrics into
[Cairn](https://github.com/johnnycube/cairn-core), using the `garminconnect`
library (Garth SSO) since Garmin has no public activity OAuth API.

### Added
- Activity import: `discover` (paged listing) and `fetch_source` (one activity
  with its stream); reconcile jobs report a watermark and enqueue fetches for
  missing activities.
- Health metrics import (`import_metrics`): HRV, sleep, weight, steps, and
  resting heart rate as typed metric events.
- Cairn NATS control plane: job consumers on `cairn.jobs.*.garmin`, protojson
  `JobResult` publishing, capability-manifest heartbeats to the
  worker-presence KV.
- Claim-checked results with fail-fast failure envelopes carrying the true
  error reason.
- Per-user credentials delivered via the server credentials channel
  (`cairn.creds.garmin.get`); env-var credentials remain as a dev fallback.
- No dependency on cairn-core: the shared contract is the committed proto
  stubs under `proto/` plus the NATS subjects.

### Known limitations
- Some field mappings are lightly verified against the live Garmin API —
  expect minor key tweaks as real-world data surfaces edge cases.

## [0.1.0] — 2026-06-26

Initial development (internal pre-release iterations v0.1.0–v0.1.5).

[0.3.2]: https://github.com/opencairn-org/cairn-provider-garmin/releases/tag/v0.3.2
[0.2.0]: https://github.com/johnnycube/cairn-provider-garmin/releases/tag/v0.2.0
