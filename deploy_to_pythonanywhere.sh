#!/bin/bash

# PythonAnywhere Deployment Script
# This script pulls the latest code, installs dependencies, runs migrations,
# collects static files, and reloads the web app

set -e  # Exit on error

echo "=== Starting PythonAnywhere Deployment ==="
echo "Timestamp: $(date)"

# Configuration - These will be set via environment variables
PROJECT_DIR="${PYTHONANYWHERE_PROJECT_DIR:-/home/yourusername/django-ecommerce-project}"
VENV_DIR="${PYTHONANYWHERE_VENV_DIR:-/home/yourusername/.virtualenvs/django-ecommerce-env}"
WEBAPP_NAME="${PYTHONANYWHERE_WEBAPP_NAME:-yourusername.pythonanywhere.com}"
PYTHONANYWHERE_USERNAME="${PYTHONANYWHERE_USERNAME:-yourusername}"
PYTHONANYWHERE_API_TOKEN="${PYTHONANYWHERE_API_TOKEN}"

# Navigate to project directory
echo ">>> Navigating to project directory: $PROJECT_DIR"
cd "$PROJECT_DIR" || { echo "Error: Project directory not found"; exit 1; }

# Pull latest code from master branch
echo ">>> Pulling latest code from GitHub..."
git fetch origin

# Check if there are local changes
if ! git diff-index --quiet HEAD --; then
    echo "⚠ Warning: Local changes detected. Creating backup..."
    BACKUP_BRANCH="backup-$(date +%Y%m%d-%H%M%S)"
    git branch "$BACKUP_BRANCH"
    echo "✓ Backup branch created: $BACKUP_BRANCH"
fi

# Reset to origin/master
git reset --hard origin/master
echo "✓ Code updated successfully"

# Activate virtual environment
echo ">>> Activating virtual environment: $VENV_DIR"
source "$VENV_DIR/bin/activate" || { echo "Error: Failed to activate virtual environment"; exit 1; }

# Install/update dependencies
echo ">>> Installing/updating dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ Dependencies installed successfully"

# Run database migrations
echo ">>> Running database migrations..."
python manage.py migrate --noinput
echo "✓ Migrations completed successfully"

# Collect static files
echo ">>> Collecting static files..."
python manage.py collectstatic --noinput
echo "✓ Static files collected successfully"

# Reload web app using PythonAnywhere API
if [ -n "$PYTHONANYWHERE_API_TOKEN" ]; then
    echo ">>> Reloading web app: $WEBAPP_NAME"
    curl -X POST \
        -H "Authorization: Token $PYTHONANYWHERE_API_TOKEN" \
        "https://www.pythonanywhere.com/api/v0/user/$PYTHONANYWHERE_USERNAME/webapps/$WEBAPP_NAME/reload/" \
        -w "\nHTTP Status: %{http_code}\n"
    
    if [ $? -eq 0 ]; then
        echo "✓ Web app reloaded successfully"
    else
        echo "⚠ Warning: Failed to reload web app via API"
        exit 1
    fi
else
    echo "⚠ Warning: PYTHONANYWHERE_API_TOKEN not set, skipping web app reload"
    echo "   Please reload the web app manually from PythonAnywhere dashboard"
fi

echo "=== Deployment Completed Successfully ==="
echo "Timestamp: $(date)"
