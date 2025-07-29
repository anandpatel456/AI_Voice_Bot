import streamlit as st
import time
from voice_utils import text_to_speech
from chains.interview_chain import generate_feedback

st.title("📋 Interview Feedback")
st.markdown("View your AI-generated interview feedback here.")

if "chat_history" not in st.session_state or not st.session_state.chat_history:
    st.warning("No interview data found. Please complete the interview first.")
else:
    with st.spinner("📝 Generating AI feedback..."):
        feedback = generate_feedback(st.session_state.chat_history)
        st.subheader("📋 Interview Feedback")
        st.write(feedback)
        text_to_speech("Here is your feedback.")
        text_to_speech(feedback)
    st.success("✅ Feedback generated successfully.")
    time.sleep(5)  # Wait for 5 seconds
    st.switch_page("Home.py")