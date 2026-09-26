FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim AS builder

WORKDIR /app

COPY pyproject.toml uv.lock ./

ENV UV_NO_DEV=1

# 2 run to keep the cache : if the project change but not the dependencies, we don't restart from scratch
RUN uv sync --frozen --no-install-project

COPY src ./src
COPY alembic ./alembic
COPY alembic.ini ./alembic.ini

RUN uv sync --frozen

FROM python:3.14-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:python3.14-bookworm-slim /uv /uvx /bin/

COPY --from=builder /app /app

ENV UV_NO_DEV=1

WORKDIR /app
EXPOSE 8000

CMD ["sh", "-c", "uv run alembic upgrade head && uv run uvicorn dbdmanager_backend.main:app --host 0.0.0.0 --port 8080"]