FROM ghcr.io/astral-sh/uv:python3.12-bookworm

WORKDIR /app

COPY .python-version .
COPY pyproject.toml .
RUN uv sync


COPY .env .

COPY src/ .

CMD [ "uv", "run", "fastapi", "run", "main.py"]