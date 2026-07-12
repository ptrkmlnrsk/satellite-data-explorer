FROM python:3.14-slim-trixie
WORKDIR /src
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY ["pyproject.toml", "uv.lock", "./"]

ENV UV_PROJECT_ENVIRONMENT=/opt/venv
ENV UV_LINK_MODE=copy
ENV PATH="/opt/venv/bin:$PATH"

RUN uv sync --locked --no-install-project

COPY . .

RUN uv sync --locked

CMD ["uv", "run", "python", "main.py"]
