import os
import json
from tqdm import tqdm
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

# Diretório de dados
data_dir = "games"
if not os.path.exists(data_dir):
    raise FileNotFoundError(f"Diretório '{data_dir}' não encontrado.")

# Inicializa o cliente e o embedding local
embedding_fn = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
client = chromadb.Client()
collection = client.get_or_create_collection(name="games", embedding_function=embedding_fn)

# Lista arquivos JSON
file_list = [f for f in sorted(os.listdir(data_dir)) if f.endswith(".json")]

# Processa os arquivos
for file_name in tqdm(file_list, desc="Processando arquivos JSON"):
    try:
        file_path = os.path.join(data_dir, file_name)
        with open(file_path, "r", encoding="utf-8") as f:
            game = json.load(f)

        doc_id = os.path.splitext(file_name)[0]
        content = f"[{game.get('Platform', 'N/A')}] {game.get('Name', 'N/A')} ({game.get('YearOfRelease', 'N/A')}) - {game.get('Description', '')}"

        collection.add(
            ids=[doc_id],
            documents=[content],
            metadatas=[game]
        )
        print(f"✅ Adicionado com sucesso: {doc_id}")

    except Exception as e:
        print(f"❌ Erro ao processar {file_name}: {e}")
