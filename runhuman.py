import streamlit as st
import math
import builtins
import contextlib
import io
from typing import Any

from langchain_core.tools import tool
from langchain.chat_models import init_chat_model
from langgraph_codeact import create_codeact
from langgraph.checkpoint.memory import MemorySaver

# ------------------------
# Define math tools
# ------------------------
@tool
def add(a: float, b: float) -> float: return a + b

@tool
def subtract(a: float, b: float) -> float: return a - b

@tool
def multiply(a: float, b: float) -> float: return a * b

@tool
def divide(a: float, b: float) -> float: return a / b

@tool
def sin(a: float) -> float: return math.sin(a)

@tool
def cos(a: float) -> float: return math.cos(a)

@tool
def radians(a: float) -> float: return math.radians(a)

@tool
def exponentiation(a: float, b: float) -> float: return a ** b

@tool
def sqrt(a: float) -> float: return math.sqrt(a)

@tool
def ceil(a: float) -> float: return math.ceil(a)

tools = [add, subtract, multiply, divide, sin, cos, radians, exponentiation, sqrt, ceil]

# -------------------------
# Unsafe code evaluator
# -------------------------
def eval_code(code: str, _locals: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    original_keys = set(_locals.keys())
    try:
        with contextlib.redirect_stdout(io.StringIO()) as f:
            exec(code, builtins.__dict__, _locals)
        result = f.getvalue() or "<code ran, no output printed to stdout>"
    except Exception as e:
        result = f"Error during execution: {repr(e)}"
    new_keys = set(_locals.keys()) - original_keys
    new_vars = {k: _locals[k] for k in new_keys}
    return result, new_vars

# -------------------------
# LangGraph agent setup
# -------------------------
model = init_chat_model("claude-3-7-sonnet-latest", model_provider="anthropic")
code_act = create_codeact(model, tools, eval_code)
agent = code_act.compile(checkpointer=MemorySaver())

# -------------------------
# Streamlit UI
# -------------------------
st.set_page_config(page_title="LangGraph CodeAct Stream", layout="wide")
st.title("LangGraph CodeAct Agent with Streaming")
thread_id = 1

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Ask your question (math/physics/NLP)", key="user_input")

if st.button("Send"):
    if user_input:
        messages = [{"role": "user", "content": user_input}]
        st.session_state.chat_history.append(("You", user_input))

        with st.spinner("Streaming response..."):
            streamed_text = ""
            response_placeholder = st.empty()
            for typ, chunk in agent.stream(
                {"messages": messages},
                stream_mode=["values", "messages"],
                config={"configurable": {"thread_id": thread_id}},
            ):
                if typ == "messages":
                    streamed_text += chunk[0].content
                    response_placeholder.markdown(streamed_text)
                elif typ == "values":
                    st.subheader("Computed Values")
                    st.json(chunk)

        st.session_state.chat_history.append(("Agent", streamed_text))

# Display full chat history
if st.session_state.chat_history:
    st.markdown("---")
    st.subheader("Chat History")
    for role, message in st.session_state.chat_history:
        st.markdown(f"**{role}:** {message}")
