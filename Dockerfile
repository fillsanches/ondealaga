FROM ghcr.io/astral-sh/uv:0.13.9-python3.13-trixie-slim

WORKDIR /srv/onde-alaga

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev

COPY app/ ./app/

CMD [".venv/bin/python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
