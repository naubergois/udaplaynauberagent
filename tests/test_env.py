import importlib
import sys


def test_check_env_missing(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("TAVILY_API_KEY", raising=False)
    monkeypatch.delenv("CHROMA_OPENAI_API_KEY", raising=False)
    app = importlib.import_module("streamlit_app")
    importlib.reload(app)
    missing = app.check_env()
    assert "OPENAI_API_KEY" in missing
    assert "TAVILY_API_KEY" in missing
    assert "CHROMA_OPENAI_API_KEY" in missing
