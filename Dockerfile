FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir poetry

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN poetry install --no-interaction --no-ansi --no-root

COPY . /app/

RUN poetry show

EXPOSE 8000

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
