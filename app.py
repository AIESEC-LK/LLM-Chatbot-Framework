import streamlit as st
from streamlit_chat import message
from utils import create_retrieval
import os
from dotenv import load_dotenv,find_dotenv


#Headlines
st.title("Loan Support Assistant")
st.subheader("Smart Bank - Powered by TheCipherSquad")

#Sessions

if 'responses' not in st.session_state:
    st.session_state['responses'] = ["Hi! Welcome to Smart Bank Loan Support Service.\nHow can I assist you?"]

if 'requests' not in st.session_state:
    st.session_state['requests'] = []



# container for chat history
response_container = st.container()

# container for text box
textcontainer = st.container()

with textcontainer:
    query = st.text_input("Query: ", key="input")

    if query:
        with st.spinner("typing..."):
            chain = create_retrieval()
            response = chain.invoke({"input":query})
            response = response["answer"]
        st.session_state.requests.append(query)
        st.session_state.responses.append(response)
        st.session_state["query"] = ""

with response_container:
    if st.session_state['responses']:

        for i in range(len(st.session_state['responses'])):
            message(st.session_state['responses'][i],key=str(i))
            if i < len(st.session_state['requests']):
                message(st.session_state["requests"][i], is_user=True,key=str(i)+ '_user')