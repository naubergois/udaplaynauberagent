import importlib.util
import sys
import os
import shutil
import json
from tqdm import tqdm
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

import chromadb
from chromadb.config import Settings

# 🔧 Corrige uso do SQLite se necessário
if importlib.util.find_spec("pysqlite3") is not None:
    import pysqlite3
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

# 🔐 Carrega variáveis de ambiente (.env)
load_dotenv()

# 📁 Caminho de persistência local do ChromaDB
chroma_path = "chromadb"
server_url = os.getenv("CHROMA_URL", "http://localhost:8000")
# 🔌 Cria cliente local ou remoto
if server_url:
    print("🔗 Conectando ao ChromaDB remoto via CHROMA_URL...")
    from urllib.parse import urlparse
    parsed = urlparse(server_url)
    host = parsed.hostname or "localhost"
    port = parsed.port or 8000
    chroma_client = chromadb.HttpClient(host=host, port=port, ssl=parsed.scheme == "https")
else:
    if os.path.exists(chroma_path):
        shutil.rmtree(chroma_path)
        print("🧹 Banco ChromaDB resetado.")
    chroma_client = chromadb.PersistentClient(path=chroma_path)

# 🤖 Modelo local para embeddings
modelo_local = SentenceTransformer("all-MiniLM-L6-v2")

# 🧱 Cria coleção SEM função de embedding (vamos gerar manualmente)
collection = chroma_client.get_or_create_collection(name="udaplay")

# 📂 Diretório com arquivos JSON
data_dir = "games"
if not os.path.exists(data_dir):
    raise FileNotFoundError(f"❌ Diretório '{data_dir}' não encontrado.")

# 📄 Lista arquivos JSON
file_list = [f for f in sorted(os.listdir(data_dir)) if f.endswith(".json")]

# 🔁 Processa arquivos
for file_name in tqdm(file_list, desc="Processando arquivos JSON"):
    try:
        file_path = os.path.join(data_dir, file_name)
        with open(file_path, "r", encoding="utf-8") as f:
            game = json.load(f)

        doc_id = os.path.splitext(file_name)[0]
        content = f"[{game.get('Platform', 'N/A')}] {game.get('Name', 'N/A')} ({game.get('YearOfRelease', 'N/A')}) - {game.get('Description', '')}"
        clean_metadata = json.loads(json.dumps(game, ensure_ascii=False))

        # 🧠 Gera embedding local manualmente
        embedding = modelo_local.encode([content])[0].tolist()

        print(embedding)

        # ➕ Adiciona ao Chroma
        collection.add(
            ids=[doc_id],
            documents=[content],
            embeddings=[embedding],  # importante: precisa ser lista de listas
            metadatas=[clean_metadata]
        )

        print(f"✅ Adicionado com sucesso: {doc_id}")
    except Exception as e:
        print(f"❌ Erro ao processar {file_name}: {e}")
