import streamlit as st
from langchain.chat_models import ChatAnthropic
from langgraph_codeact import create_codeact
from langgraph.checkpoint.memory import MemorySaver
from tools import tools
import builtins
import contextlib
import io
from typing import Any
from tools import tools  # No error now


st.set_page_config(page_title="CodeAct Agent with Stream", layout="wide")
st.title("🧠 CodeAct Agent with Human-in-the-Loop")

# Code sandbox eval
def sandbox_eval(code: str, _locals: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    original_keys = set(_locals.keys())
    try:
        with contextlib.redirect_stdout(io.StringIO()) as f:
            exec(code, builtins.__dict__, _locals)
        result = f.getvalue() or "<code ran, no output printed to stdout>"
    except Exception as e:
        result = f"Error during execution: {repr(e)}"

    new_keys = set(_locals.keys()) - original_keys
    new_vars = {key: _locals[key] for key in new_keys}
    return result, new_vars

# Model
model = ChatAnthropic(model="claude-3-7-sonnet-20240229", temperature=0)

# Build agent
code_act = create_codeact(model, tools, sandbox_eval)
agent = code_act.compile(checkpointer=MemorySaver())

# User input
user_query = st.text_input("💬 Enter your question:", "What is sin(45°) + 3^2?")

if st.button("Run Agent"):
    if user_query:
        messages = [{"role": "user", "content": user_query}]
        st.subheader("🤖 Agent Response")
        response_placeholder = st.empty()

        full_response = ""
        for typ, chunk in agent.stream(
            {"messages": messages},
            stream_mode=["values", "messages"],
            config={"configurable": {"thread_id": 1}},
        ):
            if typ == "messages":
                content = chunk[0].content
                full_response += content
                response_placeholder.markdown(full_response)
