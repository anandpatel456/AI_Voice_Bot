import streamlit as st
import time
from resume_parser import extract_text_from_pdf
from voice_utils import speech_to_text, text_to_speech
from chains.interview_chain import run_interview, generate_feedback

st.set_page_config(page_title="AI Voice Interview Bot", layout="centered")
st.title("🎤 AI Voice Interview Bot")
st.markdown("Upload your resume to begin the voice-based AI interview.")

uploaded_file = st.file_uploader("📄 Upload your Resume (PDF)", type=["pdf"])

if uploaded_file:
    with st.spinner("📃 Extracting resume content..."):
        resume_text = extract_text_from_pdf(uploaded_file)

    st.success("✅ Resume uploaded succefully!")

    if st.button("🎙️ Start Interview"):
        st.success("Interview Started! 🎧 Say 'yes' to start")

        greeting = "Hello, I am your HR for today. I’ll be conducting your interview. Are you ready?"
        st.write(f"🧠 Bot: {greeting}")
        text_to_speech(greeting)

        confirmation = speech_to_text()
        st.write(f"🗣️ You: {confirmation}")

        if "yes" not in confirmation.lower():
            st.warning("Interview not started. Please restart and confirm readiness.")
        else:
            chat_history = []
            start_time = time.time()
            general_count = 0

            while True:
                elapsed = time.time() - start_time
                if elapsed > 15 * 60:
                    st.info("⏰ Interview time (15 minutes) is over.")
                    break

                # Determine category: 2 general, then alternate between technical/projects
                if general_count < 2:
                    category = "general"
                    general_count += 1
                else:
                    category = "technical" if len(chat_history) % 2 == 0 else "projects"

                # Ask question
                question = run_interview(resume_text, chat_history, category)
                st.write(f"🧠 Bot: {question}")
                text_to_speech(question)

                answer = speech_to_text()
                st.write(f"🗣️ You: {answer}")

                if "quit" in answer.lower() or "stop" in answer.lower():
                    st.success("Interview ended by user.")
                    break

                # Retry if unclear
                if "sorry" in answer.lower() or not answer.strip():
                    st.warning("Didn't catch that. Please repeat.")
                    answer = speech_to_text()
                    st.write(f"🗣️ You (Retry): {answer}")

                    if "quit" in answer.lower() or "stop" in answer.lower():
                        st.success("Interview ended by user.")
                        break

                chat_history.append({"question": question, "answer": answer})

            # Interview is over → Generate feedback
            with st.spinner("📝 Generating AI feedback..."):
                feedback = generate_feedback(chat_history)
                st.subheader("📋 Interview Feedback")
                st.write(feedback)
                text_to_speech(feedback)
                st.success("✅ Interview and feedback complete.")
