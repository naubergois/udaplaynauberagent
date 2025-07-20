# Only needed for Udacity workspace
# !pip install chromadb
import importlib.util
import sys

# Check if 'pysqlite3' is available before importing
if importlib.util.find_spec("pysqlite3") is not None:
    import pysqlite3
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import os
import json
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv


load_dotenv()


chroma_client = chromadb.PersistentClient(path="chromadb")

embedding_fn = embedding_functions.OpenAIEmbeddingFunction(api_key=os.getenv("CHROMA_OPENAI_API_KEY"))

collection = chroma_client.get_or_create_collection(
    name="udaplay",
    embedding_function=embedding_fn
)

import os
import json
from tqdm import tqdm  # Importa o tqdm para barra de progresso
import chromadb
from chromadb.utils import embedding_functions

# Diretório de dados
data_dir = "games"

# Verifica se diretório existe
if not os.path.exists(data_dir):
    raise FileNotFoundError(f"Diretório '{data_dir}' não encontrado.")

# Inicializa o cliente e coleção do Chroma
embedding_fn = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"),  # ou use diretamente a chave como string
    model_name="text-embedding-ada-002"
)
client = chromadb.Client()
collection = client.get_or_create_collection(name="games", embedding_function=embedding_fn)

# Lista apenas arquivos JSON
file_list = [f for f in sorted(os.listdir(data_dir)) if f.endswith(".json")]

# Itera com tqdm para mostrar progresso
for file_name in tqdm(file_list, desc="Processando arquivos JSON"):
    try:
        file_path = os.path.join(data_dir, file_name)
        with open(file_path, "r", encoding="utf-8") as f:
            game = json.load(f)

        content = f"[{game['Platform']}] {game['Name']} ({game['YearOfRelease']}) - {game['Description']}"
        doc_id = os.path.splitext(file_name)[0]

        collection.add(
            ids=[doc_id],
            documents=[content],
            metadatas=[game]
        )
    except Exception as e:
        print(f"❌ Erro ao processar {file_name}: {e}")


