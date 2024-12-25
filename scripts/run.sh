#!/bin/sh

set -e

python manage.py wait_for_db

python manage.py collectstatic --noinput

python manage.py migrate

gunicorn restaurant.wsgi:application --bind 0.0.0.0:8000 --timeout=5 --threads=10
# daphne -b 0.0.0.0 -p 8000 restaurant.asgi:application