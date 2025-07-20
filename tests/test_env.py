import importlib
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def test_check_env_missing(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("TAVILY_API_KEY", raising=False)
    app = importlib.import_module("streamlit_app")
    importlib.reload(app)
    missing = app.check_env()
    assert "OPENAI_API_KEY" in missing
    assert "TAVILY_API_KEY" in missing
