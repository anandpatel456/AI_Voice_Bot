import streamlit as st
from resume_parser import extract_text_from_pdf
from voice_utils import speech_to_text, text_to_speech
from chains.interview_chain import run_interview, generate_feedback
import time

st.set_page_config(page_title="AI Voice Interview Bot", layout="centered")
st.title("🎤 AI Voice Interview Bot")
st.markdown("Upload your resume to begin the voice-based AI interview.")

uploaded_file = st.file_uploader("📄 Upload your Resume (PDF)", type=["pdf"])

if uploaded_file:
    with st.spinner("📃 Extracting resume content..."):
        resume_text = extract_text_from_pdf(uploaded_file)

    if st.button("🎙️ Start Interview"):
        st.success("Interview Started! 🎧" \
        "Say 'yes' to start interview")

        # 🤖 Bot Introduction
        greeting = "Hello, I am your HR for today. I’ll be conducting your interview. Are you ready?"
        st.write(f"🧠 Bot: {greeting}")
        text_to_speech(greeting)

        confirmation = speech_to_text()
        st.write(f"🗣️ You: {confirmation}")

        if "yes" not in confirmation.lower():
            st.warning("Interview not started. Please restart and confirm readiness.")
        else:
            chat_history = []
            question_count = 0

            while True:
                question = run_interview(resume_text, chat_history, question_count)
                st.write(f"🧠 Bot: {question}")
                text_to_speech(question)

                answer = speech_to_text()
                st.write(f"🗣️ You: {answer}")

                # --- STOP INTERVIEW if user says "stop" or "quit" --- #
                if "quit" in answer.lower() or "stop" in answer.lower():
                    st.success("Interview ended by user.")
                    break

                if "sorry" in answer.lower() or not answer.strip():
                    st.warning("Didn't catch that. Please try again.")
                    answer = speech_to_text()
                    st.write(f"🗣️ You (Retry): {answer}")

                    # Check for stop/quit again on retry
                    if "quit" in answer.lower() or "stop" in answer.lower():
                        st.success("Interview ended by user.")
                        break

                chat_history.append({"question": question, "answer": answer})
                question_count += 1

            # ✅ Generate Feedback
            with st.spinner("📝 Generating AI feedback..."):
                feedback = generate_feedback(chat_history)
                st.subheader("📋 Interview Feedback")
                text_to_speech(feedback)
                st.success("✅ Feedback given.")
