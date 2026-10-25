# Task-runner contract (https://fleetlint.org/baseline/#task-runner-contract). `make check` is the definition of green.
SHELL := bash
.SHELLFLAGS := -euo pipefail -c
.ONESHELL:
.DEFAULT_GOAL := check-fast
MAIN_BRANCH ?= main
# Python tools (ruff, mypy, pytest, pip-audit, ...) are pinned in uv.lock; the coverage floor is in pyproject.toml.
UV          := uv run --locked
IMAGE       ?= localhost/cairn-provider-garmin:dev
# podman where available (no daemon needed), else docker
CONTAINER   ?= $(shell command -v podman >/dev/null 2>&1 && echo podman || echo docker)
# Licenses allowed for runtime dependencies (the ones shipped in the image); substring match.
LICENSES    ?= MIT;BSD;Apache;ISC;PSF;Python Software Foundation;Mozilla Public License 2.0
# Each pin carries a `# renovate:` comment so Renovate bumps it (customManagers in renovate.json5).
# renovate: datasource=github-releases depName=gitleaks/gitleaks
GITLEAKS_VERSION  ?= v8.30.1
# renovate: datasource=go depName=github.com/fleetlint/fleetlint
FLEETLINT_VERSION ?= v0.5.1
# Mutation score floor for cairn_garmin (mutmut; see [tool.mutmut] in pyproject.toml).
MUTATION_MIN ?= 60
# nats-server for the permission integration test; go install verifies it against sum.golang.org.
# renovate: datasource=go depName=github.com/nats-io/nats-server/v2
NATS_SERVER_VERSION ?= v2.15.1

.PHONY: help tools fmt lint test cover audit bench mutate build image dist check-fast check release clean

help: ## list targets
	@grep -E '^[a-z-]+:.*##' $(MAKEFILE_LIST) | awk -F':.*##' '{printf "  %-12s %s\n", $$1, $$2}'

tools: ## install the locked Python toolchain, fleetlint and nats-server (gitleaks GITLEAKS_VERSION comes from its release page)
	uv sync --locked
	go install github.com/fleetlint/fleetlint/cmd/fleetlint@$(FLEETLINT_VERSION)
	go install github.com/nats-io/nats-server/v2@$(NATS_SERVER_VERSION)

fmt: ## format and autofix in place
	$(UV) ruff format
	$(UV) ruff check --fix

lint: ## format check + ruff + mypy strict + duplication (pylint duplicate-code only), warnings as errors
	$(UV) ruff format --check
	$(UV) ruff check
	$(UV) mypy
	$(UV) pylint cairn_garmin tests

test: ## all tests
	$(UV) pytest

cover: ## tests with coverage; fails below fail_under in pyproject.toml
	$(UV) pytest --cov --cov-report=term

audit: ## vulnerabilities, licenses, unused/missing deps, lockfile, secrets
	uv lock --check
	uv export --locked --all-groups --no-emit-project --format requirements-txt -q \
	  | $(UV) pip-audit --strict --disable-pip --require-hashes -r /dev/stdin
	$(UV) pip-licenses --partial-match --allow-only="$(LICENSES)" \
	  --packages $$(uv export --locked --no-dev --no-emit-project --no-hashes --no-header --no-annotate -q | sed -E 's/[=;].*//')
	$(UV) deptry .
	gitleaks git --no-banner --redact .

bench: ## benchmarks (none yet; not part of check)
	@echo "no benchmarks"

mutate: ## mutation testing of cairn_garmin (weekly in CI, not part of check); fails below MUTATION_MIN % killed
	rm -rf mutants
	CAIRN_PROTO_PATH=$$PWD/proto $(UV) mutmut run
	$(UV) mutmut export-cicd-stats
	$(UV) python -c 'import json; s = json.load(open("mutants/mutmut-cicd-stats.json")); t = s["total"] - s["skipped"]; k = s["killed"] + s["timeout"]; p = 100 * k / t if t else 0; print(f"mutation score {p:.1f}% (minimum $(MUTATION_MIN)%)"); raise SystemExit(p < $(MUTATION_MIN))'

build: ## byte-compile the worker, then build the image and smoke-test its imports
	$(UV) python -m compileall -q cairn_garmin
	$(MAKE) image
	$(CONTAINER) run --rm --entrypoint python $(IMAGE) -c "import cairn_garmin.runtime, cairn_garmin.archive"

image: ## container image only
	$(CONTAINER) build -t $(IMAGE) .

dist: image ## the release artifact is the image; the build workflow pushes, signs and attests it

check-fast: ## before every commit (< 30 s)
	$(UV) ruff format --check
	$(UV) ruff check
	$(UV) pytest -x -q

check: lint test cover audit build ## definition of green (< 10 min)
	fleetlint check --fail-on error

release: ## refuse dirty/non-main -> check -> signed tag V (version and CHANGELOG.md section must match); pushing the tag publishes the image and the GitHub release
	@test -n "$(V)" || { echo "usage: make release V=vX.Y.Z"; exit 1; }
	@test -z "$$(git status --porcelain)" || { echo "dirty tree"; exit 1; }
	@test "$$(git branch --show-current)" = "$(MAIN_BRANCH)" || { echo "not on $(MAIN_BRANCH)"; exit 1; }
	@grep -q '^version = "$(V:v%=%)"' pyproject.toml || { echo "pyproject.toml version is not $(V:v%=%)"; exit 1; }
	@grep -q '^## \[$(V:v%=%)\]' CHANGELOG.md || { echo "CHANGELOG.md has no '## [$(V:v%=%)]' section"; exit 1; }
	$(MAKE) check
	git tag -s "$(V)" -m "$(V)"
	@echo "tagged $(V) — push with: git push origin $(V)"

clean: ## remove caches and coverage output
	rm -rf .pytest_cache .ruff_cache .mypy_cache .coverage mutants
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
