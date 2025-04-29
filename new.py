# math_agents_streamlit.py

import streamlit as st
from typing import List
from langchain.chat_models import AzureChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.tools import tool
from pydantic import BaseModel
from langchain.memory import ConversationBufferMemory

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
    temperature=0
)

# ✅ Define input schema for math operations
class MathInput(BaseModel):
    numbers: List[float]

# ✅ Define math tools
@tool(args_schema=MathInput)
def add_numbers(numbers: List[float]) -> float:
    """Adds a list of numbers."""
    return sum(numbers)

@tool(args_schema=MathInput)
def subtract_numbers(numbers: List[float]) -> float:
    """Subtracts all numbers in order."""
    result = numbers[0]
    for n in numbers[1:]:
        result -= n
    return result

@tool(args_schema=MathInput)
def multiply_numbers(numbers: List[float]) -> float:
    """Multiplies a list of numbers."""
    result = 1
    for n in numbers:
        result *= n
    return result

@tool(args_schema=MathInput)
def divide_numbers(numbers: List[float]) -> float:
    """Divides numbers in sequence (first by second, then result by next, etc.)."""
    result = numbers[0]
    for n in numbers[1:]:
        if n == 0:
            return "Division by zero error"
        result /= n
    return result

# ✅ Initialize memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# ✅ Tools list
tools = [add_numbers, subtract_numbers, multiply_numbers, divide_numbers]

# ✅ Initialize agent
agent = initialize_agent(
    tools,
    llm,
    agent="chat-conversational-react-description",
    memory=memory,
    verbose=True
)

# ✅ Streamlit UI
st.set_page_config(page_title="🧮 Math Agent", layout="centered")
st.title("🧠 Math Agent with Human in the Loop")
st.write("Enter natural language math queries. Example: `add 3 and 5` or `divide 10 by 2`.")

# ✅ Chat input
user_input = st.text_input("Your math question:")

if user_input:
    with st.spinner("🧠 Thinking..."):
        try:
            response = agent.run(user_input)
            st.success(f"🔢 Answer: {response}")
        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")

# ✅ Show memory
with st.expander("🧠 Conversation History"):
    for msg in memory.chat_memory.messages:
        st.write(f"**{msg.type.title()}:** {msg.content}")
