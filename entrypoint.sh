#!/bin/sh

# Install any new dependencies
python -m pip install --upgrade pip
python -m pip install --no-cache-dir -r requirements.txt

# Requirements for development (no need if postgres is used)
python -m pip install --no-cache-dir -r requirements.txt.dev

# Run Django database migrations
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic

# Start the Django development server
exec "$@"
