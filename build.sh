#!/bin/bash
set -o errexit

echo "Installing dependencies..."
pip install -r requirements.txt


echo "Running migrations..."
python manage.py migrate

echo "Creating Superuser..."
python manage.py createsuperuser \
  --noinput \
  --email "$DJANGO_SUPERUSER_EMAIL" \
  --username admin
echo "Superuser created."

echo "Collecting static files..."
python manage.py collectstatic --noinput