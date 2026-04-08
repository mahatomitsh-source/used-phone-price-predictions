import streamlit as st

def logout():
    st.session_state.logged_in = False
    st.session_state.clear()   # clears all session data
    st.success("✅ Logged out successfully!")
    st.rerun()