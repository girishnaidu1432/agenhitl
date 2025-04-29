import streamlit as st
import openai
import math
import builtins
import contextlib
import io
from typing import Any
from langchain.chat_models import AzureChatOpenAI
from langgraph_codeact import create_codeact

# ------------------------------------
# Azure OpenAI configuration
# ------------------------------------
openai.api_key = "14560021aaf84772835d76246b53397a"
openai.api_base = "https://amrxgenai.openai.azure.com/"
openai.api_type = "azure"
openai.api_version = "2024-02-15-preview"
deployment_name = "gpt"

# ------------------------------------
# Import tools from your tools.py
# ------------------------------------
from tools import tools

# ------------------------------------
# Sandbox (unsafe eval for demo)
# ------------------------------------
def eval_code(code: str, _locals: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    try:
        with contextlib.redirect_stdout(io.StringIO()) as f:
            exec(code, builtins.__dict__, _locals)
        output = f.getvalue() or "<code ran, no output>"
    except Exception as e:
        output = f"Error: {repr(e)}"
    return output, {}

# ------------------------------------
# AzureChatOpenAI model setup
# ------------------------------------
model = AzureChatOpenAI(
    openai_api_base=openai.api_base,
    openai_api_version=openai.api_version,
    deployment_name=deployment_name,
    openai_api_key=openai.api_key,
    openai_api_type=openai.api_type,
)

code_act = create_codeact(model, tools, eval_code)
agent = code_act.compile()

# ------------------------------------
# Streamlit UI
# ------------------------------------
st.title("🔁 CodeAct Agent with Azure OpenAI")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Ask a question:", key="user_input")

if st.button("Run"):
    if user_input:
        st.session_state.chat_history.append(("User", user_input))
        messages = [{"role": "user", "content": user_input}]

        st.info("Thinking...")
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

# ------------------------------------
# Chat History
# ------------------------------------
st.markdown("---")
for role, msg in st.session_state.chat_history:
    st.markdown(f"**{role}:** {msg}")
