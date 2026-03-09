import streamlit as st
import requests

API_URL = "http://localhost:8000/api/chat"

st.title("Personal AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.write(msg)

user_input = st.text_input("Ask something")

if st.button("Send"):

    payload = {
        "message": user_input,
        "project_id": 1
    }

    response = requests.post(API_URL, json=payload)

    data = response.json()

    answer = data["response"]

    st.session_state.messages.append("User: " + user_input)
    st.session_state.messages.append("AI: " + answer)

    st.experimental_rerun()