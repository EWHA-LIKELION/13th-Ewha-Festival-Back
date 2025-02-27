#!/bin/sh

echo "Waiting for database..."
while ! nc -z db 3306; do
  sleep 1
done
echo "Database ready!"

echo "Applying database migrations..."
python manage.py migrate accounts
python manage.py migrate admin
python manage.py migrate auth
python manage.py migrate contenttypes
python manage.py migrate sessions
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn festival.wsgi:application --bind 0.0.0.0:8000
