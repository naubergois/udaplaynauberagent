#!/usr/bin/env bash
# Setup Python virtual environment for UdaPlay project on Linux/Mac
set -e
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo
echo "Setup complete. Activate the environment with:"
echo "  source .venv/bin/activate"
