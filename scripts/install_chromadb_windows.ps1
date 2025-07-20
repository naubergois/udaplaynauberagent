# install_chromadb_windows.ps1 - Install and start ChromaDB locally on Windows.

# Install ChromaDB using pip
python -m pip install --upgrade chromadb

# Start the ChromaDB server with persistence in ./chromadb
chroma run --path ./chromadb
