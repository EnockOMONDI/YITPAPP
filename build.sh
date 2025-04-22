#!/bin/bash

# Build the project
set -o errexit  # exit on error
echo "Building the lgf."




pip install -r requirements.txt



# Create necessary directories
mkdir -p staticfiles
mkdir -p media/uploads

# Reset and recreate jet migrations
python manage.py migrate jet zero --fake
python manage.py migrate jet_dashboard zero --fake
python manage.py migrate jet --fake-initial
python manage.py migrate jet_dashboard --fake-initial

# Run all migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput