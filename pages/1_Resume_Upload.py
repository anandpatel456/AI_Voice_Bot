import streamlit as st
from resume_parser import extract_text_from_pdf
import time

st.title("📄 Resume Upload")
st.markdown("Upload your resume to begin the voice-based AI interview.")

# Initialize session state
if "resume_text" not in st.session_state:
    st.session_state.resume_text = None
if "redirected" not in st.session_state:
    st.session_state.redirected = False

uploaded_file = st.file_uploader("📄 Upload your Resume (PDF)", type=["pdf"])

if uploaded_file:
    with st.spinner("📃 Extracting resume content..."):
        try:
            st.session_state.resume_text = extract_text_from_pdf(uploaded_file)
        except Exception as e:
            st.error(f"Error extracting resume: {e}")
    if st.session_state.resume_text is not None:
        st.success("✅ Resume uploaded successfully!")
        st.session_state.redirected = True
        st.markdown("Redirecting to Interview Page...")
        time.sleep(5)
        st.switch_page("pages/2_Interview.py")
        if not st.session_state.redirected:
            st.session_state(f"Error when Redirecting!")
           