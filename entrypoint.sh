#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

# Install any new dependencies
python -m pip install --upgrade pip
python -m pip install --no-cache-dir -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
exec "$@"
