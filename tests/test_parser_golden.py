"""Pins the parsed output of every fixture archive to the parser version (core
ADR 0005). Changing the output needs a new config.VERSION: bump M, then
`CAIRN_UPDATE_GOLDEN=1 make test` writes the new version's goldens; it never
overwrites an existing one. Delete the old version's goldens afterwards.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest
from google.protobuf import json_format

from cairn_garmin import config as C
from cairn_garmin import mapping

DATA = Path(__file__).parent / "data"
ARCHIVES = sorted((DATA / "archives").glob("*.json"))


def test_fixtures_exist() -> None:
    assert ARCHIVES


@pytest.mark.parametrize("path", ARCHIVES, ids=lambda p: p.stem)
def test_parser_golden(path: Path) -> None:
    env = json.loads(path.read_text())
    assert env["version"] == C.DATASET_VERSION
    events = mapping.parse_archive(
        env, user_id="u1", account_id="a1", ext_id=str(env["activity"]["activityId"]), blob_id="blob-1"
    )
    got = json.dumps([json_format.MessageToDict(e) for e in events], indent=2, sort_keys=True) + "\n"

    golden = DATA / "golden" / f"{path.stem}.parser-{C.VERSION}.json"
    others = [g for g in (DATA / "golden").glob(f"{path.stem}.parser-*.json") if g != golden]
    assert not others, f"stale goldens of an older parser: {others}"
    if not golden.exists():
        if os.environ.get("CAIRN_UPDATE_GOLDEN"):
            golden.write_text(got)
            return
        pytest.fail(f"no golden for parser {C.VERSION}: run with CAIRN_UPDATE_GOLDEN=1")
    assert got == golden.read_text(), f"parsed output changed under parser {C.VERSION}: bump VERSION (M)"
