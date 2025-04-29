import openai
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain_core.tools import tool
from langgraph_codeact import create_codeact
from tools import tools  # Assuming tools.py is in the same directory
from langchain.memory import ConversationBufferMemory

# Set up OpenAI API details
openai.api_key = "14560021aaf84772835d76246b53397a"
openai.api_base = "https://amrxgenai.openai.azure.com/"
openai.api_type = 'azure'
openai.api_version = '2024-02-15-preview'
deployment_name = 'gpt'

# Initialize Streamlit app interface
st.title('Human-in-the-loop Mathematical Agent')
st.write('Ask any math-related question, and I will help solve it step by step.')

# Initialize memory with ConversationBufferMemory
memory = ConversationBufferMemory(memory_key="conversation_history", return_messages=True)

# Set up model
model = ChatOpenAI(model="gpt-4", openai_api_key=openai.api_key)

# Create a CodeAct agent
code_act = create_codeact(model, tools, eval)
agent = code_act.compile()

# Function to process user input
def process_input(user_input):
    # Add user message to memory
    memory.add_user_message(user_input)

    # Get agent response
    response = agent.invoke({"messages": [{"role": "user", "content": user_input}]})

    # Display the response
    st.write(f"Agent's Response: {response['messages'][0]['content']}")

    # Add response to memory
    memory.add_ai_message(response['messages'][0]['content'])

    return response['messages'][0]['content']

# Main interaction loop
user_input = st.text_input("Ask me anything:")

if user_input:
    with st.spinner("Processing..."):
        agent_response = process_input(user_input)
        
        # Give feedback and ask for follow-up
        follow_up = st.text_input("Would you like to ask something more or clarify?")

        if follow_up:
            with st.spinner("Processing..."):
                follow_up_response = process_input(follow_up)
                st.write(f"Agent's Follow-up Response: {follow_up_response}")

# Display the conversation history
st.write("**Conversation History**:")
st.write(memory.load_memory_variables({}))
