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

# Remove the reference to .svg files in the Font Awesome CSS
sed -i'.bak' '/\.svg/d' static/assets/css/fontAwesome5Pro.css

# Collect static files
python manage.py collectstatic --noinput