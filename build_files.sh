#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Run migrations
python crowcrows/manage.py migrate

# Collect static files
python crowcrows/manage.py collectstatic --noinput

# Ensure all the required permissions are set
chmod -R 755 crowcrows/staticfiles
