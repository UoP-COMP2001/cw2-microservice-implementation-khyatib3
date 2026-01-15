#!/bin/bash
set -e

# Start the application
echo "Starting ProfileService API on 0.0.0.0:8000..."
echo "Swagger UI will be available at http://localhost:8000/profileservice-api/ui/"
exec python app.py
