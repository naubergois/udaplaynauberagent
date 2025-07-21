import importlib.util
import sys
import os
import json
from typing import List, Dict
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from pydantic import BaseModel
import chromadb
from chromadb.utils import embedding_functions
from chromadb.config import Settings
from lib.tooling import tool
from lib.game_agent import GameAgent

# 🛠 Corrige SQLite no Udacity workspace (ou outros ambientes com pysqlite3)
if importlib.util.find_spec("pysqlite3") is not None:
    import pysqlite3
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

# 🔐 Carrega variáveis de ambiente
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# 🤖 Modelo de embedding local
modelo_local = SentenceTransformer("all-MiniLM-L6-v2")

@tool(name="retrieve_game", description="Semantic search: Finds most results in the vector DB")
def retrieve_game(query: str) -> List[Dict]:
    """Search game information from the local vector database."""
    client = chromadb.PersistentClient(path="chromadb")
    collection = client.get_or_create_collection(name="udaplay")

    # Gera embedding manualmente
    query_embedding = modelo_local.encode([query])[0].tolist()

    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=3,
        include=["documents", "metadatas"]
    )

    documents = result.get("documents", [[]])[0]
    metadatas = result.get("metadatas", [[]])[0]

    games = []
    for doc, meta in zip(documents, metadatas):
        game = {
            "Name": meta.get("Name"),
            "Platform": meta.get("Platform"),
            "YearOfRelease": meta.get("YearOfRelease"),
            "Description": meta.get("Description"),
        }
        games.append(game)

    return games

class EvaluationReport(BaseModel):
    useful: bool
    description: str

@tool(name="evaluate_retrieval", description="Based on the user's question and on the list of retrieved documents, analyze if they can answer the question")
def evaluate_retrieval(question: str, retrieved_docs: List[str]) -> EvaluationReport:
    """Assess if retrieved docs are enough to answer the question."""
    from lib.llm import LLM
    from lib.parsers import PydanticOutputParser

    llm = LLM(model="gpt-4o-mini")
    docs = "\n".join(retrieved_docs)
    prompt = (
        "Your task is to evaluate if the documents are enough to respond the query. "
        "Give a detailed explanation, so it's possible to take an action to accept it or not.\n"
        f"# Question:\n{question}\n# Documents:\n{docs}\nRespond with JSON."
    )

    ai_message = llm.invoke(prompt)
    parser = PydanticOutputParser(model_class=EvaluationReport)
    try:
        report = parser.parse(ai_message)
    except Exception:
        content = ai_message.content or ""
        useful = "yes" in content.lower()
        report = EvaluationReport(useful=useful, description=content)
    return report

@tool(name="game_web_search", description="Tavily web search for additional info")
def game_web_search(question: str) -> List[Dict]:
    """Perform a Tavily web search for additional information."""
    import requests

    api_key = TAVILY_API_KEY
    if not api_key:
        raise ValueError("Missing TAVILY_API_KEY")

    url = "https://api.tavily.com/search"
    payload = {"api_key": api_key, "query": question, "search_depth": "basic"}
    resp = requests.post(url, json=payload, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return data.get("results", [])

# 🔄 Executa agente
# 🔄 Executa agente
agent = GameAgent()

# Consulta 1
res1 = agent.invoke("When Pokémon Gold and Silver was released?")
print("\n📌 Resultado 1: Pokémon Gold and Silver")
print(res1)

# Consulta 2
res2 = agent.invoke("Which one was the first 3D platformer Mario game?")
print("\n📌 Resultado 2: First 3D Mario platformer")
print(res2)

# Consulta 3
res3 = agent.invoke("Was Mortal Kombat X released for Playstation 5?")
print("\n📌 Resultado 3: Mortal Kombat X on PS5")
print(res3)
