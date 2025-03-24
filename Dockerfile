ARG PYTHON_VERSION=3.12.8
FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y postgresql-client

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/app" \
    appuser

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && poetry install --only main --no-interaction --no-root

COPY . .

RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

#FROM python:3.12-slim
#
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1
#
#RUN apt-get update && apt-get install -y --no-install-recommends \
#    libpq-dev curl \
#    && rm -rf /var/lib/apt/lists/*
#
#RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir poetry
#
#WORKDIR /app
#
#COPY pyproject.toml poetry.lock* /app/
#
#RUN poetry install --no-interaction --no-ansi --no-root
#
#COPY . /app/
#
#RUN poetry show
#
#EXPOSE 8000
#
#CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
