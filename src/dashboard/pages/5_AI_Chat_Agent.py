import streamlit as st

st.set_page_config(page_title="AI Chat Agent", page_icon="🤖", layout="wide")

st.title("🤖 AI Career Agent")

st.markdown("Ask our AI agent anything about the job market, resume optimization, or learning paths.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("E.g., What are the top skills? Which jobs match my resume?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Mock agent response. In the future, this calls our LangChain agent!
    response = f"I am the Data Engineering AI Agent. You asked: '{prompt}'. \n\n*Note: This is a placeholder response until the LangChain backend is fully integrated!*"
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
