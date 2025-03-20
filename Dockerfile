FROM python:3.12-slim

# environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# directory
WORKDIR /app

# system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

# Poetry
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir poetry

# Copy only Poetry files
COPY pyproject.toml poetry.lock* /app/

# project dependencies using Poetry
RUN poetry install --no-interaction --no-ansi

COPY . /app/

# Expose port 8000
EXPOSE 8000

ENTRYPOINT ["poetry", "run", "python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
