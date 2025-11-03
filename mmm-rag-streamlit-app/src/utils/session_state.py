from streamlit import session_state as st_session

def get_session_state():
    if 'messages' not in st_session:
        st_session.messages = []
    if 'user_input' not in st_session:
        st_session.user_input = ""
    return st_session.messages, st_session.user_input

def set_user_input(user_input):
    st_session.user_input = user_input

def add_message(role, content):
    st_session.messages.append({"role": role, "content": content})