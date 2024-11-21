#!/bin/bash

# Check if pyenv is installed
if ! command -v pyenv &> /dev/null; then
    echo "pyenv is not installed. Please install pyenv first."
    echo "Mac: brew install pyenv pyenv-virtualenv"
    exit 1
fi

# Install Python 3.11.8 if not already installed
pyenv install 3.11.8 --skip-existing

# Create virtualenv named 'step1' using Python 3.11.8
pyenv virtualenv 3.11.8 step1

# Set local Python version to step1 environment
cd "$(dirname "$0")"  # Move to script directory
pyenv local step1

# Install required packages
pip install fastapi "uvicorn[standard]" streamlit requests

# Create required directories
mkdir -p backend frontend