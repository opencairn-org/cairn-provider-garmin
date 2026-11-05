"""Entrypoint for the Cairn Garmin worker."""

from __future__ import annotations

import logging

from cairn_provider_sdk import serve

from . import config as C
from .runtime import Worker


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    # Credentials are fetched per account via cairn.creds.garmin.get; the env
    # values are only a single-account dev fallback.
    serve(Worker(C.load()))


if __name__ == "__main__":
    main()
