#!/bin/sh

echo "Waiting for database..."
while ! pg_isready -h db -p 5432 -U $POSTGRES_USER; do
  sleep 1
done

echo "Database is ready!"

python manage.py migrate

exec python manage.py runserver 0.0.0.0:8000
