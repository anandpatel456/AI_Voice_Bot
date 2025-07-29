import streamlit as st
import time
st.set_page_config(page_title="AI Voice Interview Bot", layout="centered")
st.title("🏠 Home")
st.markdown("Welcome to the AI Voice Interview Bot.")
st.subheader("✅ Unlock your potential with AI 🚀🧠 – Empower your personal growth through smart technology! 🌱💡")



# Redirect to Resume Upload page with debugging
if "redirected" not in st.session_state:
    st.session_state.redirected = False
if not st.session_state.redirected:
    st.session_state.redirected = True
    time.sleep(8)
    st.write("Redirecting to Resume Upload...")
    st.switch_page("pages/1_Resume_Upload.py")