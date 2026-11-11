# syntax=docker/dockerfile:1@sha256:4edf897a3ffa55b89f906fc8cc78afdb3f1834cc9c7083565e611a8a7d5fe99e
# Base images are pinned by digest; Renovate bumps tag and digest together.
FROM docker.io/library/python:3.14-slim@sha256:9aaa474097d094040649f2162a627c0049b408f52138d980916788d80f04802f AS deps
COPY --from=ghcr.io/astral-sh/uv:0.13.1@sha256:4a1f3666816dafadd20ceb71eac9a7d56d7ef30279f7d64048519ab901ada336 /uv /bin/uv
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/opt/venv
WORKDIR /app
# Runtime dependencies exactly as locked in uv.lock (cairn-provider-sdk is the
# wheel from its GitHub release, checked against the locked hash).
COPY pyproject.toml uv.lock .python-version ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-install-project

FROM docker.io/library/python:3.14-slim@sha256:9aaa474097d094040649f2162a627c0049b408f52138d980916788d80f04802f
RUN useradd --uid 10001 --user-group --no-create-home --home-dir /data --shell /usr/sbin/nologin cairn \
    && mkdir -p /data/garth && chown -R cairn: /data
WORKDIR /app
COPY --from=deps /opt/venv /opt/venv
# Worker package; the contract stubs come with the SDK in the venv.
COPY cairn_garmin ./cairn_garmin
# Release tag for the core compatibility check (core ADR 0005); CI passes the tag.
ARG VERSION=docker
RUN printf '%s\n' "$VERSION" > /app/cairn_garmin/RELEASE

ENV PATH=/opt/venv/bin:$PATH \
    PYTHONPATH=/app \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    CAIRN_GARTH_HOME=/data/garth

USER 10001
VOLUME ["/data"]
ENTRYPOINT ["python", "-m", "cairn_garmin.main"]
