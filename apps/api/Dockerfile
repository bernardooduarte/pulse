FROM python:3.12-slim AS base
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

COPY pyproject.toml alembic.ini ./
COPY src ./src
COPY alembic ./alembic
RUN pip install --no-cache-dir .

EXPOSE 8000
CMD alembic upgrade head && uvicorn pulse_api.interface.main:app --host 0.0.0.0 --port "${PORT:-8000}"
