#!/bin/sh

# database migrations
echo "Apply database migrations..."
python manage.py migrate 

# running Django check
echo "Running Django check..."
python manage.py check

# collect static files
echo "Collect static files..."
python manage.py collectstatic --noinput

# Start Gunicorn processes
echo Starting Gunicorn...
exec gunicorn core.wsgi:application \
    --bind "0.0.0.0:8000" \
    --workers 3 \
    --timeout 300
    