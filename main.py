import streamlit as st
import requests
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
import os

username= os.getenv("API_USERNAME")
password=os.getenv("API_PASSWORD")
endpoint =os.getenv("API_ENDPOINT")
st.session_state.authenticated = True
st.set_page_config(page_title="Fashion", layout="wide")
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """

st.markdown(hide_st_style, unsafe_allow_html=True)

def creds_entered():
    
    if st.session_state["user"].strip() == "admin" and st.session_state["password"].strip() == "genaifashion":
        st.session_state["authenticated"] = True
    else:
        st.session_state["authenticated"] = False
        if not st.session_state["password"]:
            st.warning("Please enter password.")
        elif not st.session_state["user"]:
            st.warning("Please enter username.")
        else:
            st.error("Invalid username and password :face_with_raised_eyebrow:")
        
def authenticate_user():
    if "authenticated" not in st.session_state:
        username = st.text_input(label="Username:", value="", key="user")
        password = st.text_input(label="Password:", value="", key="password", type="password")
        submit = st.button("Submit", on_click=creds_entered)

        if submit and username == "admin" and password == "password":
            st.session_state.authenticated = True

        return False
    else:
        if st.session_state.authenticated:
            return True
        else:
            username = st.text_input(label="Username:", value="", key="user")
            password = st.text_input(label="Password:", value="", key="password", type="password")
            submit = st.button("Submit", on_click=creds_entered)

            if submit and username == "admin" and password == "password":
                st.session_state.authenticated = True

            return False


if authenticate_user():
    with st.sidebar:
        uploaded_file = st.file_uploader("Bir resim yükleyin", type=["jpg", "png"])
        if uploaded_file is not None:
            st.image(uploaded_file, caption='Your image', use_column_width=True)



    user_question = st.chat_input("Enter your message")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []   
    
    for message in st.session_state.messages:
        with st.chat_message(message.get("role")):
            st.write(message.get("content"))
    
    if user_question:
        if uploaded_file is None:
            st.error("Bir resim yükleyin.")
    
    if uploaded_file is not None:
        if user_question:
            st.session_state.messages.append({"role": "user", "content": user_question})
            with st.chat_message("user"):
                st.write(user_question)
            spinner = st.spinner("Thinking...") 
            url = endpoint + "/api/v1/uid/gpt4v"
            files = {'input_image': uploaded_file.getvalue()}
            try:
                with spinner:
                    response = requests.post(url, files=files, params={"question": user_question})
                    print(response.json())
                    response = (response.json()["message"]["content"])
                    st.session_state.messages.append({"role": "assistant", "content": response})
                with st.chat_message("assistant"):
                    st.write(response)
            
            except Exception as e:
                st.error("An error occurred. Please try again later. {e}")


