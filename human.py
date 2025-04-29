import openai
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain_core import tool
from langgraph_codeact import create_codeact
from tools import tools
from langchain.agents import Tool

# Set up OpenAI API
openai.api_key = "your-openai-api-key"
openai.api_base = "https://amrxgenai.openai.azure.com/"
openai.api_type = 'azure'
openai.api_version = '2024-02-15-preview'
deployment_name = 'gpt'

# Initialize LangGraph Agent
def initialize_langgraph_agent():
    model = ChatOpenAI(model="gpt-4", openai_api_key=openai.api_key)
    code_act = create_codeact(model, tools, eval)
    agent = code_act.compile(checkpointer=None)
    return agent

# Function to process user input
def process_input(user_input):
    memory_context = st.session_state.get('memory', [])
    
    # Add user message to context
    memory_context.append({"role": "user", "content": user_input})
    st.session_state['memory'] = memory_context
    
    agent = initialize_langgraph_agent()
    messages = [{"role": "system", "content": "You are a helpful assistant."}] + memory_context
    response = agent.invoke({"messages": messages})
    
    return response

# Streamlit UI
def display_chat():
    st.title("Human-in-the-Loop Agent")
    
    if 'memory' not in st.session_state:
        st.session_state['memory'] = []
    
    user_input = st.text_input("Enter your question:")
    
    if user_input:
        agent_response = process_input(user_input)
        
        # Display agent's response
        st.write(f"Agent: {agent_response}")
        
        # Allow user to give feedback or correct the agent
        feedback = st.text_input("Provide feedback or corrections:")
        if feedback:
            st.session_state['memory'].append({"role": "assistant", "content": feedback})

if __name__ == "__main__":
    display_chat()
