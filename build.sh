#!/bin/bash

# YITP Django Application Build Script for Render
set -o errexit  # exit on error

echo "🚀 Building YITP Django Application (Development Branch)..."
echo "================================================"

# Check Python version
echo "🐍 Python version:"
python --version

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Verify critical imports
echo "🔍 Verifying critical imports..."
python -c "
import django
print(f'✅ Django version: {django.get_version()}')

import shortuuid
print('✅ shortuuid imported successfully')

import pyuploadcare
print('✅ pyuploadcare imported successfully')

import psycopg2
print('✅ psycopg2 imported successfully')
"

# Detailed repository and environment diagnostics
echo "🔍 Repository and Environment Diagnostics..."
echo "================================================"

# Show current working directory
echo "📁 Current working directory:"
pwd

# Show directory contents
echo "📋 Root directory contents:"
ls -la

# Show Python path
echo "🐍 Python path:"
python -c "import sys; print('\n'.join(sys.path))"

# Check if blogapp directory exists
echo "🔍 Checking for blogapp directory:"
if [ -d "blogapp" ]; then
    echo "✅ blogapp directory exists"
    echo "📋 blogapp directory contents:"
    ls -la blogapp/

    # Check specific files
    echo "🔍 Checking critical blogapp files:"
    for file in "__init__.py" "apps.py" "models.py" "views.py" "urls.py"; do
        if [ -f "blogapp/$file" ]; then
            echo "  ✅ blogapp/$file exists"
        else
            echo "  ❌ blogapp/$file missing"
        fi
    done
else
    echo "❌ blogapp directory does not exist!"
    echo "📋 Available directories:"
    find . -maxdepth 1 -type d -name "*app*" -o -name "*blog*" | head -10
fi

# Check other Django apps
echo "� Checking other Django app directories:"
for app in "users" "yitp" "events"; do
    if [ -d "$app" ]; then
        echo "  ✅ $app directory exists"
    else
        echo "  ❌ $app directory missing"
    fi
done

# Test Django app imports with detailed error reporting
echo "�🔧 Testing Django app imports with detailed diagnostics..."
python -c "
import os
import sys
import traceback

print(f'🐍 Python executable: {sys.executable}')
print(f'📁 Current working directory: {os.getcwd()}')
print(f'📋 Directory contents: {os.listdir(\".\")}')

# Add current directory to Python path
sys.path.insert(0, os.getcwd())
print(f'🛤️  Updated Python path: {sys.path[:3]}...')

# Check if blogapp directory exists from Python
if os.path.exists('blogapp'):
    print('✅ blogapp directory exists (Python check)')
    print(f'📋 blogapp contents: {os.listdir(\"blogapp\")}')

    # Check __init__.py
    if os.path.exists('blogapp/__init__.py'):
        print('✅ blogapp/__init__.py exists')
        with open('blogapp/__init__.py', 'r') as f:
            content = f.read()
            print(f'📄 __init__.py content length: {len(content)} characters')
    else:
        print('❌ blogapp/__init__.py missing')
else:
    print('❌ blogapp directory does not exist (Python check)')

# Test individual app imports with detailed error handling
print('\\n🔧 Testing imports...')
try:
    print('🔍 Attempting to import blogapp...')
    import blogapp
    print('✅ blogapp module imported successfully')
    print(f'📍 blogapp module location: {blogapp.__file__}')

    print('🔍 Attempting to import blogapp.apps...')
    import blogapp.apps
    print('✅ blogapp.apps imported successfully')

    print('🔍 Attempting to import BlogappConfig...')
    from blogapp.apps import BlogappConfig
    print('✅ BlogappConfig imported successfully')
    print(f'📍 BlogappConfig: {BlogappConfig}')

except ImportError as e:
    print(f'❌ Import error: {e}')
    print('🔍 Full traceback:')
    traceback.print_exc()

    # Additional debugging
    print('\\n🔍 Additional debugging information:')
    print(f'📁 Current directory files: {[f for f in os.listdir(\".\") if not f.startswith(\".\")}')

    # Try to find any *app* directories
    app_dirs = [d for d in os.listdir('.') if os.path.isdir(d) and 'app' in d.lower()]
    print(f'📁 Directories containing \"app\": {app_dirs}')

    sys.exit(1)
"

# Check Django configuration
echo "🔧 Checking Django configuration..."
python manage.py check

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