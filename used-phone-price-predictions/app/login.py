import streamlit as st
import json
from pathlib import Path

# -----------------------
# Load Users
# -----------------------
BASE_DIR = Path(__file__).resolve().parent
USERS_PATH = BASE_DIR.parent / "auth" / "users.json"

def load_users():
    if USERS_PATH.exists():
        with open(USERS_PATH, "r") as f:
            return json.load(f)
    return {}

# -----------------------
# Login Page
# -----------------------
def login_page():

    st.markdown("""
    <style>

    @import url('https://fonts.googleapis.com/css?family=Noto+Sans+TC&display=swap');

    /* Background */
    .stApp {
        background: radial-gradient(#a429bc,#9225a7,#7f2092);
        font-family: 'Noto Sans TC', sans-serif;
    }

    /* Center everything */
    [data-testid="stAppViewContainer"] {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }

    /* Main container */
    .center-box {
        width: 430px;
    }

    /* Header */
    .header-box {
        font-size: 28px;
        font-weight: bold;
        color: white;
        padding: 25px;
        background: #5c1769;
        border-radius: 10px 10px 0 0;
    }

    /* Form box */
    .form-box {
        background: white;
        padding: 30px;
        border-radius: 0 0 10px 10px;
    }

    /* Inputs */
    .stTextInput {
        margin-bottom: 20px;
    }

    .stTextInput input {
        border: none;
        border-bottom: 2px solid #ccc;
        border-radius: 0;
        padding: 10px;
        font-size: 15px;
    }

    .stTextInput input:focus {
        border-bottom: 2px solid #7f2092;
        outline: none;
    }

    /* Button */
    .stButton>button {
        margin-top: 20px;
        width: 130px;
        height: 45px;
        color: white;
        cursor: pointer;
        border-radius: 25px;
        border: none;
        background: #5c1769;
        display: block;
        margin-left: auto;
    }

    .stButton>button:hover {
        background: #491254;
        transition: .5s;
    }

    /* Forgot link */
    .forgot {
        font-size: 16px;
        color: #7f2092;
        margin-top: 15px;
        display: block;
        text-decoration: none;
    }

    .forgot:hover {
        text-decoration: underline;
    }

    </style>
    """, unsafe_allow_html=True)

    # -------- UI --------
    st.markdown('<div class="center-box">', unsafe_allow_html=True)

    st.markdown('<div class="header-box">Login Form</div>', unsafe_allow_html=True)

    st.markdown('<div class="form-box">', unsafe_allow_html=True)

    username = st.text_input("Email or Username")

    # 👁 Show password toggle (replacement for JS)
    show = st.checkbox("Show Password")
    password = st.text_input("Password", type="default" if show else "password")

    users = load_users()

    if st.button("Sign in"):
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.success("Login successful ✅")
            st.rerun()
        else:
            st.error("Invalid username or password ❌")

    st.markdown('<a class="forgot" href="#">Forgot Password?</a>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # form-box
    st.markdown('</div>', unsafe_allow_html=True)  # center-box