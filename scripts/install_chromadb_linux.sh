#!/usr/bin/env bash
# install_chromadb_linux.sh - Install and start ChromaDB locally on Linux.
set -e

# Install ChromaDB using pip
python3 -m pip install --upgrade chromadb

# Start the ChromaDB server with persistence in ./chromadb
exec chroma run --path ./chromadb
