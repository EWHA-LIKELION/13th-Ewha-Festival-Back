#!/bin/sh
# python manage.py collectstatic --no-input echo "Apply database migrations" python manage.py migrate
python manage.py collectstatic --no-input
python manage.py migrate contenttypes --fake-initial
python manage.py migrate auth --fake-initial
python manage.py migrate accounts --fake-initial
python manage.py migrate admin --fake-initial
python manage.py migrate sessions --fake-initial
python manage.py migrate --fake-initial
python manage.py makemigrations
python manage.py migrate
exec "$@"