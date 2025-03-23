#!/bin/sh

# Install any new dependencies
python -m pip install --upgrade pip
python -m pip install --no-cache-dir -r requirements.txt

# Run Django database migrations
echo "Building migration files"
python manage.py makemigrations

echo "Running migrations"
python manage.py migrate

echo "Collecting staticfiles"
python manage.py collectstatic --noinput

echo "Creating superuser"
python manage.py createsuperuser --noinput

# Start the Django development server
exec "$@"
