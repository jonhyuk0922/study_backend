#!/bin/bash

# Check if pyenv is installed
if ! command -v pyenv &> /dev/null; then
    echo "pyenv is not installed. Please install pyenv first."
    echo "Mac: brew install pyenv pyenv-virtualenv"
    exit 1
fi

# Install Python 3.11.8 if not already installed
pyenv install 3.11.8 --skip-existing

# Create virtualenv named 'step2' using Python 3.11.8
pyenv virtualenv 3.11.8 step2

# Set local Python version to step2 environment
cd "$(dirname "$0")"  # Move to script directory
pyenv local step2

# Upgrade pip
pip install --upgrade pip

# Install required packages for both frontend and backend
pip install fastapi "uvicorn[standard]" streamlit requests python-dotenv

# Install LangChain related packages
pip install langchain
pip install langchain-openai
pip install langchain-core
pip install langchain-community
pip install openai

# Create required directories
mkdir -p backend frontend chat_histories

# Create empty __init__.py files
touch backend/__init__.py
touch frontend/__init__.py

echo "Setup completed successfully!"