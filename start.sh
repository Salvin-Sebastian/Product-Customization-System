#!/usr/bin/env bash
# Start Celery worker in the background with limited concurrency to save memory
celery -A config worker --loglevel=info --concurrency=1 &

# Start Gunicorn web server in the foreground
gunicorn config.wsgi:application
