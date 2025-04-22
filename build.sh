#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
mkdir -p staticfiles
mkdir -p media/uploads

# First, fake the initial migrations for jet since tables already exist
python manage.py migrate jet zero --fake
python manage.py migrate jet --fake-initial

# Then run all other migrations
python manage.py migrate --fake-initial

# Collect static files
python manage.py collectstatic --noinput