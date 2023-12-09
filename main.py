import streamlit as st
import requests


def main():
    st.set_page_config(page_title="My streamlit app")
           
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
                
            url = "http://4.255.89.202/api/v1/vision" 
            files = {'image': uploaded_file.getvalue()}
            response = requests.post(url, files=files, params={"question": user_question})
            response = (response.json()['gpt']["choices"][0]["message"]["content"])
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            with st.chat_message("assistant"):
                st.write(response)
            

if __name__ == '__main__':
    main()