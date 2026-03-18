FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONPATH=/api \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_CACHE_DIR=/api/.cache/uv \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_LINK_MODE=copy

WORKDIR /api

RUN adduser --disabled-password --gecos "" --home "/api" --shell "/sbin/nologin" --no-create-home --uid 1000 app
RUN mkdir -p $UV_CACHE_DIR && chown -R app:app /api

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=$UV_CACHE_DIR \
    uv sync --frozen --no-install-project --no-dev --all-extras --verbose

ARG TEST=false

RUN --mount=type=cache,target=$UV_CACHE_DIR \
    if [ "$TEST" = "true" ] ; then \
    uv sync --frozen --no-install-project --all-extras; \
    fi

RUN chown -R app:app /api

USER app

ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 5000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
