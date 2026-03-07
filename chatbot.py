from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq
import base64


# load the env variables
load_dotenv()

# Load logo as base64
with open("assets/theRiseTheoryLogo.PNG", "rb") as f:
    logo_data = base64.b64encode(f.read()).decode()

# streamlit page setup
st.set_page_config(
    page_title="The Rise Theory Chatbot",
    page_icon="assets/theRiseTheoryLogo.PNG",
    layout="centered",
)

# --- custom CSS --------------------------------------------------------------
st.markdown(
    """
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .chat-message {
        margin: 10px 0;
        padding: 10px 15px;
        border-radius: 15px;
        white-space: normal;
    }
    .chat-message.user {
        color: white;
        text-align: left;
    }
    .chat-message.assistant {
        color: white;
        text-align: left;
    }
    .stChatMessage {
        display: flex;
        flex-direction: column;
        margin-bottom: 10px;
    }
    .stMarkdown > p {
        margin: 0;
    }
    .header {
        text-align: center;
        padding: 20px;
        background-color: white;
        border-bottom: 1px solid #e0e0e0;
    }
    .header h1 {
        margin: 0;
        color: #333;
    }
    .st-emotion-cache-1ir3vnm.e1ypd8m71 {
        margin: 0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Display title
st.markdown(f'''
<div class="header">
    <img src="data:image/png;base64,{logo_data}" style="display: block; margin: 0 auto; width: 80px; height: auto;">
    <h1>RiseTheoryGPT</h1>
</div>
''', unsafe_allow_html=True)

# initiate chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# display history inside a container
chat_container = st.container()
with chat_container:
    for message in st.session_state.chat_history:
        role = message["role"]
        content = message["content"]
        with st.chat_message(role):
            st.markdown(f'<div class="chat-message {role}">{content}</div>',
                        unsafe_allow_html=True)

# llm initiate
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.0,
)

# keep the input at the bottom
user_prompt = st.chat_input("Your message…")

if user_prompt:
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(f'<div class="chat-message user">{user_prompt}</div>',
                    unsafe_allow_html=True)

    response = llm.invoke(
        input=[{"role": "system", "content": "You are a helpful assistant"}, *st.session_state.chat_history]
    )
    assistant_response = response.content
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    with st.chat_message("assistant"):
        st.markdown(f'<div class="chat-message assistant">{assistant_response}</div>',
                    unsafe_allow_html=True)
