import streamlit as st
import math
import builtins
import contextlib
import io
from typing import Any

from langchain_core.tools import tool
from langchain.chat_models import init_chat_model
from langgraph_codeact import create_codeact

# ------------------------
# Tools for computation
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

# ------------------------
# Simple eval sandbox (unsafe for production)
# ------------------------
def eval_code(code: str, _locals: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    try:
        with contextlib.redirect_stdout(io.StringIO()) as f:
            exec(code, builtins.__dict__, _locals)
        output = f.getvalue() or "<code ran, no output>"
    except Exception as e:
        output = f"Error: {repr(e)}"
    return output, {}

# ------------------------
# Agent setup
# ------------------------
model = init_chat_model("claude-3-7-sonnet-latest", model_provider="anthropic")
code_act = create_codeact(model, tools, eval_code)
agent = code_act.compile()

# ------------------------
# Streamlit UI
# ------------------------
st.title("🔁 LangGraph CodeAct Agent")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Enter your question:", key="input")

if st.button("Submit"):
    if user_input:
        st.session_state.chat_history.append(("User", user_input))
        messages = [{"role": "user", "content": user_input}]
        
        st.info("Generating response...")
        response_placeholder = st.empty()
        response_text = ""

        for typ, chunk in agent.stream(
            {"messages": messages},
            stream_mode=["values", "messages"]
        ):
            if typ == "messages":
                response_text += chunk[0].content
                response_placeholder.markdown(response_text)
            elif typ == "values":
                st.subheader("🔢 Computed Values")
                st.json(chunk)

        st.session_state.chat_history.append(("Agent", response_text))

# Display history
st.markdown("---")
for role, msg in st.session_state.chat_history:
    st.markdown(f"**{role}:** {msg}")
