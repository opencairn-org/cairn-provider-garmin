# Contributing to cairn-provider-garmin

Contributions are welcome. For anything beyond a small fix, open an issue first
so the direction is agreed before the work starts.

## License of contributions

The project is Apache-2.0. By submitting a contribution you agree it is licensed
under the same terms (Section 5 of the Apache License). There is no CLA.

Sign off every commit (`git commit -s`) to assert the
[Developer Certificate of Origin](https://developercertificate.org/).

## Setup

Prerequisites: [uv](https://docs.astral.sh/uv/), `make`, Go (to install
fleetlint), [gitleaks](https://github.com/gitleaks/gitleaks/releases) and
podman or docker for the image build.

```bash
make tools        # uv sync --locked (Python and all dev tools from uv.lock) + fleetlint
prek install      # git hooks from .pre-commit-config.yaml
```

## Working rules

- `make check` must pass: ruff format and lint, mypy strict, the tests with the
  coverage floor from `pyproject.toml`, pip-audit on the locked dependencies,
  the runtime license allowlist, deptry, `uv lock --check`, gitleaks, the image
  build with an import smoke test, and fleetlint. CI runs the same target.
  `make check-fast` is the quick loop before a commit.
- Dependencies change through `uv add` / `uv lock`; commit `pyproject.toml` and
  `uv.lock` together.
- Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/);
  the commit-msg hook enforces it. `main` is changed through pull requests only.
- `proto/` is generated from the Cairn proto contract. Regenerate the
  `_pb2.py` modules and their `_pb2.pyi` stubs together (`--python_out` and
  `--pyi_out`) and do not edit them by hand.
- Mapping changes come with a test using a real (anonymised) Garmin response
  shape; `cairn_garmin/mapping.py` documents the quirks seen so far.

## Releases

Update the version in `pyproject.toml` and add a `## [X.Y.Z]` section to
`CHANGELOG.md`, then on `main` run `make release V=vX.Y.Z` and push the tag.
The build workflow re-runs `make check`, publishes the signed image and
creates the GitHub release (CHANGELOG section as notes, SBOM attached).
