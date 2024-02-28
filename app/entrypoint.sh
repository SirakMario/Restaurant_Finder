#!/bin/bash

# Function to check if PostgreSQL is ready
is_postgres_ready() {
  pg_isready -h database -U user -d mydb -q
}

# Wait for PostgreSQL to be ready
until is_postgres_ready; do
  echo "PostgreSQL is not ready yet. Waiting..."
  sleep 5
done
echo "PostgreSQL is ready now."

# Apply database migrations
python manage.py makemigrations
python manage.py migrate
python manage.py load_restaurants

# Start the Django development server
python manage.py runserver 0.0.0.0:8000

