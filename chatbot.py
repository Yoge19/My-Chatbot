import streamlit as st
import ollama
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)

# Set up Streamlit page config
st.set_page_config(page_title="Chatbot", page_icon="🤖")
st.title("🤖 Simple Chatbot")

# Initialize session state for messages
if "messages" not in st.session_state or not isinstance(st.session_state.messages, list):
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    if "role" in msg and "content" in msg:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    else:
        logging.warning(f"Invalid message format: {msg}")

# Input box for new user message
user_input = st.chat_input("Type your message here...")

# Only proceed if user has entered input
if user_input:
    # Save and display the user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        logging.info(f"User input: {user_input}")
        st.markdown(user_input)

    # Prepare message history for API call
    try:
        validated_messages = []
        for m in st.session_state.messages:
            if isinstance(m.get("content"), str) and isinstance(m.get("role"), str):
                validated_messages.append({"role": m["role"], "content": m["content"]})
            else:
                logging.warning(f"Invalid message format: {m}")

        # Call Ollama API
        response = ollama.chat(
            model="llama3",
            messages=validated_messages
        )

        logging.info(f"Full API response: {response}")

        # Parse the assistant's reply
        if "message" in response and "content" in response["message"]:
            reply = response["message"]["content"].strip()
            if not reply:
                reply = "Sorry, I didn't understand that."
        else:
            logging.warning(f"Unexpected response format: {response}")
            reply = "Sorry, I didn't understand that."

    except Exception as e:
        reply = "Sorry, I couldn't process your request. Please try again later."
        st.error(f"Error: {e}")
        logging.error(f"Exception: {e}")

    # Save and display the assistant reply
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
        logging.info(f"Assistant reply: {reply}")