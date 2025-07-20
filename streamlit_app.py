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
from lib.game_agent import GameAgent, report_run
import io
import contextlib


def check_env() -> list[str]:
    """Return list of missing environment keys required for the agent."""
    required = ["OPENAI_API_KEY", "TAVILY_API_KEY"]
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

    if "history" not in st.session_state:
        st.session_state["history"] = []

    for item in st.session_state["history"]:
        st.write(f"**You:** {item['question']}")
        st.write(f"**Agent:** {item['answer']}")
        with st.expander("Debug"):
            st.code(item["debug"])
        st.write("---")

    query = st.text_input("Ask a question about video games")
    if st.button("Ask") and query:
        agent = GameAgent()
        with st.spinner("Thinking..."):
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                run = agent.invoke(query)
                report_run(run)
            debug_output = buf.getvalue()
        final = run.get_final_state()
        answer = final.get("answer") if final else None
        if answer:
            st.session_state["history"].append(
                {"question": query, "answer": answer, "debug": debug_output}
            )
            st.write(answer)
            with st.expander("Debug"):
                st.code(debug_output)
        else:
            st.write("No answer available.")


if __name__ == "__main__":
    main()
