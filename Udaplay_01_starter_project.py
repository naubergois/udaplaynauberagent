import importlib.util
import sys
import os
import shutil
import json
from tqdm import tqdm
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

# 🛠️ Corrige o uso do SQLite se necessário
if importlib.util.find_spec("pysqlite3") is not None:
    import pysqlite3
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

# 🔐 Carrega variáveis do .env (especialmente OPENAI_API_KEY)
load_dotenv()

# 📁 Diretório de persistência do ChromaDB
chroma_path = "chromadb"
if os.path.exists(chroma_path):
    shutil.rmtree(chroma_path)
    print("🧹 Banco ChromaDB resetado.")

# 📁 Diretório com arquivos JSON
data_dir = "games"
if not os.path.exists(data_dir):
    raise FileNotFoundError(f"❌ Diretório '{data_dir}' não encontrado.")

# 🚀 Inicializa o cliente com persistência
chroma_client = chromadb.PersistentClient(path=chroma_path)

# 🧠 Define função de embedding via OpenAI
embedding_fn = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="text-embedding-ada-002"
)

# 🧱 Cria coleção com a função de embedding explícita (ESSENCIAL!)
collection = chroma_client.get_or_create_collection(
    name="udaplay",
    embedding_function=embedding_fn
)

# 📥 Lista arquivos JSON
file_list = [f for f in sorted(os.listdir(data_dir)) if f.endswith(".json")]

# 🔄 Processa os arquivos
for file_name in tqdm(file_list, desc="Processando arquivos JSON"):
    try:
        file_path = os.path.join(data_dir, file_name)
        with open(file_path, "r", encoding="utf-8") as f:
            game = json.load(f)

        doc_id = os.path.splitext(file_name)[0]
        content = f"[{game.get('Platform', 'N/A')}] {game.get('Name', 'N/A')} ({game.get('YearOfRelease', 'N/A')}) - {game.get('Description', '')}"

        # 🔧 Corrige possíveis tipos inválidos nos metadados
        clean_metadata = json.loads(json.dumps(game, ensure_ascii=False))

        collection.add(
            ids=[doc_id],
            documents=[content],
            metadatas=[clean_metadata]
        )
        print(f"✅ Adicionado com sucesso: {doc_id}")

    except Exception as e:
        print(f"❌ Erro ao processar {file_name}: {e}")
