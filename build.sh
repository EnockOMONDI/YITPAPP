#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p staticfiles
mkdir -p media/uploads

# Remove existing migrations (optional, use with caution)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# Make fresh migrations
python manage.py makemigrations jet
python manage.py makemigrations jet_dashboard
python manage.py makemigrations

# Apply migrations
python manage.py migrate jet
python manage.py migrate jet_dashboard
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput