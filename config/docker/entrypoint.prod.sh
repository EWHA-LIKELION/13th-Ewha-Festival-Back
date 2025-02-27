#!/bin/sh

echo "Waiting for database..."
until nc -z db 3306; do
  sleep 2
  echo "Waiting for MySQL to be ready..."
done

echo "Database is ready! Running migrations..."
python manage.py migrate contenttypes --fake-initial
python manage.py migrate auth --fake-initial
python manage.py migrate accounts --fake-initial
python manage.py migrate admin --fake-initial
python manage.py migrate sessions --fake-initial
python manage.py migrate --fake-initial

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn festival.wsgi:application --bind 0.0.0.0:8000
