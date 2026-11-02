# syntax=docker/dockerfile:1@sha256:4edf897a3ffa55b89f906fc8cc78afdb3f1834cc9c7083565e611a8a7d5fe99e
# Base images are pinned by digest; Renovate bumps tag and digest together.
FROM docker.io/library/python:3.14-slim@sha256:cd89c30eda26ee911a4611b18680086e0ea42e6f5f8cbe653d07fa7958c9cec8 AS deps
COPY --from=ghcr.io/astral-sh/uv:0.13.1@sha256:4a1f3666816dafadd20ceb71eac9a7d56d7ef30279f7d64048519ab901ada336 /uv /bin/uv
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/opt/venv
WORKDIR /app
# Runtime dependencies exactly as locked in uv.lock.
COPY pyproject.toml uv.lock .python-version ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-install-project

FROM docker.io/library/python:3.14-slim@sha256:cd89c30eda26ee911a4611b18680086e0ea42e6f5f8cbe653d07fa7958c9cec8
RUN useradd --uid 10001 --user-group --no-create-home --home-dir /data --shell /usr/sbin/nologin cairn \
    && mkdir -p /data/garth && chown -R cairn: /data
WORKDIR /app
COPY --from=deps /opt/venv /opt/venv
# Worker package + the committed generated proto stubs it imports.
COPY cairn_garmin ./cairn_garmin
COPY proto /opt/cairn-proto
# Release tag for the core compatibility check (core ADR 0005); CI passes the tag.
ARG VERSION=docker
RUN printf '%s\n' "$VERSION" > /app/cairn_garmin/RELEASE

ENV PATH=/opt/venv/bin:$PATH \
    PYTHONPATH=/app \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    CAIRN_PROTO_PATH=/opt/cairn-proto \
    CAIRN_GARTH_HOME=/data/garth

USER 10001
VOLUME ["/data"]
ENTRYPOINT ["python", "-m", "cairn_garmin.main"]
