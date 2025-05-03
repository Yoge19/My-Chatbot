import streamlit as st
import ollama

# Set up Streamlit page configuration
st.set_page_config(page_title="Local Llama Chatbot")

st.title("🤖 Local Llama Chatbot")
st.write("Ask anything and I'll respond using Llama 3 locally!")

# Store conversation in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input box
user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get the response from Llama 3 model using Ollama API
    response = ollama.chat(model="llama2", messages=[
        {"role": "user", "content": user_input}
    ])
    
    # Extract and display the response
    reply = response['text']
    st.session_state.messages.append({"role": "assistant", "content": reply})
    
    with st.chat_message("assistant"):
        st.markdown(reply)