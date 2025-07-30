#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Check if the database file exists. If not, run the init script.
if [ ! -f "serviceonwheel.db" ]; then
  echo "Database not found. Initializing..."
  python database.py
else
  echo "Database already exists. Skipping initialization."
fi

# Start the Gunicorn server
exec gunicorn app:app
