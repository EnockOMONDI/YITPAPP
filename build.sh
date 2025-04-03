#!/bin/bash

# Build the project
set -o errexit  # exit on error
echo "Building the lgf."




pip install -r requirements.txt

python manage.py collectstatic --noinput 

python manage.py makemigrations 
python manage.py migrate 
