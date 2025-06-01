#!/bin/bash

# Build the project
set -o errexit  # exit on error
echo "Building your app sean, final moments to go live."




pip install -r requirements.txt

python manage.py collectstatic 

python manage.py makemigrations 
python manage.py migrate 



