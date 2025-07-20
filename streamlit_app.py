import os
try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - provide fallback when dotenv not installed
    def load_dotenv(*args, **kwargs):
        return False

try:
    import streamlit as st
except ImportError:  # pragma: no cover - provide minimal streamlit stub
    class _DummySpinner:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            pass

    class _DummyStreamlit:
        def error(self, *args, **kwargs):
            pass

        def stop(self):
            pass

        def title(self, *args, **kwargs):
            pass

        def text_input(self, *args, **kwargs):
            return ""

        def button(self, *args, **kwargs):
            return False

        def spinner(self, *args, **kwargs):
            return _DummySpinner()

        def write(self, *args, **kwargs):
            pass

    st = _DummyStreamlit()
from lib.game_agent import GameAgent


def check_env() -> list[str]:
    """Return list of missing environment keys required for the agent."""
    required = ["OPENAI_API_KEY", "TAVILY_API_KEY", "CHROMA_OPENAI_API_KEY"]
    return [k for k in required if not os.getenv(k)]


def main():
    if not load_dotenv():
        load_dotenv("config.env")
    missing = check_env()
    if missing:
        st.error(
            "Missing the following API keys: "
            + ", ".join(missing)
            + ". Please update your .env file and restart."
        )
        st.stop()

    st.title("UdaPlay Game Agent")
    query = st.text_input("Ask a question about video games")
    if st.button("Ask") and query:
        agent = GameAgent()
        with st.spinner("Thinking..."):
            run = agent.invoke(query)
        final = run.get_final_state()
        answer = final.get("answer") if final else None
        if answer:
            st.write(answer)
        else:
            st.write("No answer available.")


if __name__ == "__main__":
    main()
