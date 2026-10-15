FROM ghcr.io/astral-sh/uv:0.13.1-python3.14-trixie-slim AS builder

WORKDIR /app

COPY pyproject.toml uv.lock ./

ENV UV_NO_DEV=1

# 2 run to keep the cache : if the project change but not the dependencies, we don't restart from scratch
RUN uv sync --frozen --no-install-project

COPY src ./src
COPY alembic ./alembic
COPY alembic.ini ./alembic.ini
COPY README.md ./README.md

RUN uv sync --frozen

FROM python:3.14-slim-trixie

COPY --from=ghcr.io/astral-sh/uv:0.13.1 /uv /uvx /bin/

COPY --from=builder /app /app

ENV UV_NO_DEV=1

WORKDIR /app
EXPOSE 8000

CMD ["sh", "-c", "uv run alembic upgrade head && uv run uvicorn dbdmanager_backend.main:app --reload --host 0.0.0.0 --port 8000"]