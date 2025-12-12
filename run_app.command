#!/bin/bash

# YouTubeサムネイル生成ツール起動スクリプト (macOS/Linux)

cd "$(dirname "$0")"

# Check if venv exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate venv
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
.venv/bin/pip install -r app/requirements.txt --quiet

# Run the app
echo "Starting YouTubeサムネイル生成ツール..."
.venv/bin/python app/main.py
