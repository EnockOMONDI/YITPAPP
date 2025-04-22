#!/usr/bin/env bash
# exit on error
set -o errexit

# Clean Python cache
find . -type d -name "__pycache__" -exec rm -r {} +
find . -type f -name "*.pyc" -delete

# Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
mkdir -p staticfiles
mkdir -p media/uploads

# Remove existing migrations for jet
find . -path "*/jet/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/jet/migrations/*.pyc" -delete

# Make fresh migrations
python manage.py makemigrations

# Apply migrations in the correct order
python manage.py migrate auth
python manage.py migrate contenttypes
python manage.py migrate admin
python manage.py migrate sessions
python manage.py migrate jet
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput