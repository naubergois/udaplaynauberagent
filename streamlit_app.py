import os
from dotenv import load_dotenv
import streamlit as st
from lib.game_agent import GameAgent


def check_env() -> list[str]:
    """Return list of missing environment keys required for the agent."""
    required = ["OPENAI_API_KEY", "TAVILY_API_KEY", "CHROMA_OPENAI_API_KEY"]
    return [k for k in required if not os.getenv(k)]


def main():
    load_dotenv("config.env")
    missing = check_env()
    if missing:
        st.error(
            "Missing the following API keys: "
            + ", ".join(missing)
            + ". Please update config.env and restart."
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
