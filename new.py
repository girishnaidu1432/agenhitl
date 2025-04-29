# streamlit_app.py

import streamlit as st
from langchain.chat_models import AzureChatOpenAI
from langchain.tools import tool
from langchain.memory import ConversationBufferMemory
import json

# ✅ Azure OpenAI Configuration
openai_api_key = "14560021aaf84772835d76246b53397a"
openai_api_base = "https://amrxgenai.openai.azure.com/"
openai_api_type = "azure"
openai_api_version = "2024-02-15-preview"
deployment_name = "gpt"

llm = AzureChatOpenAI(
    deployment_name=deployment_name,
    openai_api_key=openai_api_key,
    openai_api_base=openai_api_base,
    openai_api_type=openai_api_type,
    openai_api_version=openai_api_version,
    temperature=0.5
)

# ✅ Memory initialization
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(return_messages=True)

# ✅ Math Tools
@tool
def add_numbers(args: str) -> str:
    """Add two numbers. Input format: "5,3"."""
    try:
        a, b = map(float, args.split(","))
        return f"Sum: {a + b}"
    except:
        return "❌ Error: Use format 'number1,number2'"

@tool
def subtract_numbers(args: str) -> str:
    """Subtract two numbers. Input format: "10,4"."""
    try:
        a, b = map(float, args.split(","))
        return f"Difference: {a - b}"
    except:
        return "❌ Error: Use format 'number1,number2'"

@tool
def multiply_numbers(args: str) -> str:
    """Multiply two numbers. Input format: "2,6"."""
    try:
        a, b = map(float, args.split(","))
        return f"Product: {a * b}"
    except:
        return "❌ Error: Use format 'number1,number2'"

@tool
def divide_numbers(args: str) -> str:
    """Divide two numbers. Input format: "8,2"."""
    try:
        a, b = map(float, args.split(","))
        if b == 0:
            return "❌ Error: Cannot divide by zero"
        return f"Quotient: {a / b}"
    except:
        return "❌ Error: Use format 'number1,number2'"

# ✅ Tool list
tools = [add_numbers, subtract_numbers, multiply_numbers, divide_numbers]

# ✅ Supervisor Agent
def supervisor_agent(prompt: str) -> str:
    steps = []
    prompt_lower = prompt.lower()

    if "add" in prompt_lower:
        steps.append(("Addition", add_numbers))
    elif "subtract" in prompt_lower:
        steps.append(("Subtraction", subtract_numbers))
    elif "multiply" in prompt_lower:
        steps.append(("Multiplication", multiply_numbers))
    elif "divide" in prompt_lower:
        steps.append(("Division", divide_numbers))
    else:
        return "❌ Please specify a math operation like add, subtract, multiply, or divide."

    results = []
    for desc, func in steps:
        user_input = st.text_input(f"Step: {desc} - Enter numbers (e.g., 4,2)", key=desc)
        if user_input:
            result = func.run(user_input)
            results.append(f"{desc}: {result}")
            st.session_state.memory.chat_memory.add_user_message(f"{desc} of {user_input}")
            st.session_state.memory.chat_memory.add_ai_message(result)
            st.success(result)

    return "\n".join(results)

# ✅ Streamlit UI
st.title("🧠 Math Agents with Human-in-the-Loop + Memory")

st.write("Enter a prompt like:")
st.code("Add two numbers", language="text")

user_prompt = st.text_input("🔍 Your instruction")

if user_prompt:
    with st.spinner("Running..."):
        result = supervisor_agent(user_prompt)
        st.markdown("### ✅ Result")
        st.write(result)

st.markdown("---")
st.markdown("### 🧠 Memory Log")
for msg in st.session_state.memory.buffer:
    st.markdown(f"- **{msg.type.upper()}**: {msg.content}")
