#!/bin/bash

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment 'venv' not found. Please create it first using: python -m venv venv OR python virtualenv venv"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Export environment variables
export FLASK_DEBUG=1

# Run Flask
flask run