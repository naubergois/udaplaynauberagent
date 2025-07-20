from __future__ import annotations
import os
import json
from typing import List, Dict
try:
    from pydantic import BaseModel
except ImportError:  # pragma: no cover - fallback when pydantic is missing
    import json

    class BaseModel:
        def __init__(self, **data):
            for k, v in data.items():
                setattr(self, k, v)

        @classmethod
        def model_validate_json(cls, json_str: str):
            return cls(**json.loads(json_str))

        def dict(self):
            return self.__dict__
try:
    import chromadb
    if not hasattr(chromadb, "PersistentClient"):
        # Handle case where a local directory named 'chromadb' shadows the
        # actual package or an outdated version is installed.
        chromadb = None
except ImportError:  # pragma: no cover - allow running without chromadb
    chromadb = None
from lib.tooling import tool

# We expect the vector DB to be persisted in ./chromadb and the collection named 'udaplay'

@tool(name="retrieve_game", description="Semantic search: Finds most results in the vector DB")
def retrieve_game(query: str) -> List[Dict]:
    """Search game information from the local vector database."""
    if chromadb is None:  # pragma: no cover - dependency unavailable
        return []

    server_url = os.getenv("CHROMA_URL")
    if server_url:
        try:
            from urllib.parse import urlparse
            parsed = urlparse(server_url)
            host = parsed.hostname or "localhost"
            port = parsed.port or 8000
            client = chromadb.HttpClient(host=host, port=port, ssl=parsed.scheme == "https")
        except Exception:
            client = chromadb.HttpClient(server_url)
    else:
        client = chromadb.PersistentClient(path="chromadb")
    collection = client.get_collection("udaplay")
    result = collection.query(query_texts=[query], n_results=3, include=["documents", "metadatas"])
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
        f"# Question:\n{question}\n# Documents:\n{docs}\nRespond with JSON." )

    ai_message = llm.invoke(prompt)
    parser = PydanticOutputParser(model_class=EvaluationReport)
    try:
        report = parser.parse(ai_message)
    except Exception:
        # fallback simple parse
        content = ai_message.content or ""
        useful = "yes" in content.lower()
        report = EvaluationReport(useful=useful, description=content)
    return report

@tool(name="game_web_search", description="Semantic search: Finds most results in the vector DB")
def game_web_search(question: str) -> List[Dict]:
    """Perform a Tavily web search for additional information."""
    try:
        import requests
    except ImportError:  # pragma: no cover - requests not installed
        return []

    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise ValueError("Missing TAVILY_API_KEY")
    url = "https://api.tavily.com/search"
    payload = {"api_key": api_key, "query": question, "search_depth": "basic"}
    resp = requests.post(url, json=payload, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return data.get("results", [])

