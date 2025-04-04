#!/bin/sh
IP="${1:-0.0.0.0}"
PORT="${2:-8000}"

echo "Initializing my application"

poetry run python3 manage.py migrate
#TODO: test_data in staging seite einbauen ?

echo "Starting my application on ${IP}:${PORT}..."
poetry run gunicorn --bind ${IP}:${PORT} economic_comparison.wsgi:application
