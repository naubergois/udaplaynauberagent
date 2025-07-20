from dotenv import load_dotenv
import os

from lib.vector_db import VectorStoreManager, CorpusLoaderService


def main():
    load_dotenv()
    manager = VectorStoreManager(persist_directory="chromadb")
    loader = CorpusLoaderService(manager)

    store = loader.load_games("udaplay", "games")
    manager.persist()

    query = "When was Pokémon Gold released?"
    result = store.query([query], n_results=3)

    for doc, meta in zip(result["documents"][0], result["metadatas"][0]):
        print(f"{meta['Name']} ({meta['Platform']}) - {meta['YearOfRelease']}")
        print(doc)
        print()


if __name__ == "__main__":
    main()
