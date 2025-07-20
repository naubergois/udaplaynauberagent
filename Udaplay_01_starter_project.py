<<<<<<< HEAD
import os
import json
from tqdm import tqdm
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

# Diretório de dados
data_dir = "games"
=======
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

embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

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
>>>>>>> 2103e1d73b975ed93657d3b7332b73aa82884795
if not os.path.exists(data_dir):
    raise FileNotFoundError(f"Diretório '{data_dir}' não encontrado.")

# Inicializa o cliente e coleção do Chroma
<<<<<<< HEAD
embedding_fn = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"),  # ou use diretamente a chave como string
    model_name="text-embedding-ada-002"
=======
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
>>>>>>> 2103e1d73b975ed93657d3b7332b73aa82884795
)
client = chromadb.Client()
collection = client.get_or_create_collection(name="games", embedding_function=embedding_fn)

<<<<<<< HEAD
# Lista arquivos JSON
file_list = [f for f in sorted(os.listdir(data_dir)) if f.endswith(".json")]

# Processa os arquivos
=======
# Lista apenas arquivos JSON
file_list = [f for f in sorted(os.listdir(data_dir)) if f.endswith(".json")]

# Itera com tqdm para mostrar progresso
>>>>>>> 2103e1d73b975ed93657d3b7332b73aa82884795
for file_name in tqdm(file_list, desc="Processando arquivos JSON"):
    try:
        file_path = os.path.join(data_dir, file_name)
        with open(file_path, "r", encoding="utf-8") as f:
            game = json.load(f)

<<<<<<< HEAD
        doc_id = os.path.splitext(file_name)[0]
        content = f"[{game.get('Platform', 'N/A')}] {game.get('Name', 'N/A')} ({game.get('YearOfRelease', 'N/A')}) - {game.get('Description', '')}"
=======
        content = f"[{game['Platform']}] {game['Name']} ({game['YearOfRelease']}) - {game['Description']}"
        doc_id = os.path.splitext(file_name)[0]
>>>>>>> 2103e1d73b975ed93657d3b7332b73aa82884795

        collection.add(
            ids=[doc_id],
            documents=[content],
            metadatas=[game]
        )
<<<<<<< HEAD
        print(f"✅ Adicionado com sucesso: {doc_id}")

    except Exception as e:
        print(f"❌ Erro ao processar {file_name}: {e}")
=======
    except Exception as e:
        print(f"❌ Erro ao processar {file_name}: {e}")


>>>>>>> 2103e1d73b975ed93657d3b7332b73aa82884795
