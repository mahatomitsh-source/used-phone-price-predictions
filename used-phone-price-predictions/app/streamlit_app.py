import streamlit as st
from login import login_page
from dashboard import dashboard
from dashboard import prediction

st.set_page_config(
    page_title="Phone Price Predictor",
    page_icon="📱",
    layout="wide"
)

# session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# -----------------------
# MAIN SYSTEM
# -----------------------

if st.session_state.logged_in == False:

    login_page()

else:

    st.sidebar.title("Navigation")

    page = st.sidebar.selectbox(
        "Menu",
        ["Dashboard","Prediction","Logout"]
    )

    if page == "Dashboard":
        dashboard()

    elif page == "Prediction":
        prediction()

    elif page == "Logout":

        st.session_state.logged_in = False
        st.rerun()