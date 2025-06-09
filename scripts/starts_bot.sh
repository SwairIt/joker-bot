#!/bin/bash

MAIN="../src/joker_bot/main.py"

echo "Check dependencies..."
poetry check || poetry install

if [ ! -f "$MAIN" ]; then
    echo "Error: Main script not found at $MAIN"
    exit 1
fi

poetry run python3 "$MAIN"