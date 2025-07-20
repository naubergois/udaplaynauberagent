import importlib
import sys
import os
import types

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def test_game_agent_runs(monkeypatch):
    dummy = types.SimpleNamespace()

    class DummyCompletion:
        @staticmethod
        def create(**kwargs):
            class Response:
                choices = [
                    types.SimpleNamespace(
                        message=types.SimpleNamespace(content="answer")
                    )
                ]
                usage = None

            return Response()

    dummy.OpenAI = lambda api_key=None: types.SimpleNamespace(
        chat=types.SimpleNamespace(completions=DummyCompletion)
    )
    monkeypatch.setitem(sys.modules, "openai", dummy)

    # Reload dependencies to ensure patched openai is used
    importlib.invalidate_caches()
    if "lib.llm" in sys.modules:
        importlib.reload(sys.modules["lib.llm"])

    ga = importlib.import_module("lib.game_agent")
    importlib.reload(ga)

    agent = ga.GameAgent()
    run = agent.invoke("Who made Mario?")
    final = run.get_final_state()
    assert final.get("answer") == "answer"
