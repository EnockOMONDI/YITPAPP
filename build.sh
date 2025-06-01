#!/bin/bash

# YITP Django Application Build Script for Render
set -o errexit  # exit on error

echo "🚀 Building YITP Django Application..."
echo "================================================"

# Check Python version
echo "🐍 Python version:"
python --version

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Verify Django installation
echo "🔍 Verifying Django installation..."
python -c "import django; print(f'Django version: {django.get_version()}')"

# Check Django configuration
echo "🔧 Checking Django configuration..."
python manage.py check --deploy

# Collect static files for production
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create and apply database migrations
echo "🗄️  Preparing database migrations..."
python manage.py makemigrations --noinput

echo "🗄️  Applying database migrations..."
python manage.py migrate --noinput

# Test database connection
echo "🔍 Testing database connection..."
python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')
django.setup()
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute('SELECT 1')
    print('✅ Database connection successful')
"

# Create superuser if it doesn't exist (optional)
echo "👤 Checking for superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    print('No superuser found. You can create one after deployment.')
else:
    print('Superuser already exists.')
"

echo "✅ Build completed successfully!"
echo "🌐 YITP is ready for deployment!"
echo "================================================"