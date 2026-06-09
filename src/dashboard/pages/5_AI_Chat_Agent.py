import streamlit as st

st.set_page_config(page_title="AI Chat Agent", page_icon="🤖", layout="wide")

st.title("🤖 AI Career Agent")

st.markdown("Ask our AI agent anything about the job market, resume optimization, or learning paths.")

import os
import sys

# Add the src directory to the path so we can import the agent
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from src.agent.job_market_agent import JobMarketAgent

# Initialize the agent
@st.cache_resource
def get_agent():
    return JobMarketAgent(data_path="data/processed/jobs_with_skills.csv")

agent = get_agent()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("E.g., What are the top skills? Are there jobs in New York? Check my resume: python, sql"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Call our rule-based agent!
    response = agent.ask(prompt)
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
