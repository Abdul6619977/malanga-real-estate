#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Create a superuser if variables are provided
if [[ $DJANGO_SUPERUSER_USERNAME ]]; then
  python manage.py createsuperuser --no-input || true
fi
