import streamlit as st
import time
from voice_utils import speech_to_text, text_to_speech
from chains.interview_chain import run_interview

st.set_page_config(page_title="AI Interview", layout="centered")
st.title("🎤 Interview Session")
st.markdown("🌱 “Stay calm, be yourself, and trust your preparation. You’ve got this!”")


# 1. Ensure resume is uploaded
if "resume_text" not in st.session_state or st.session_state.resume_text is None:
    st.warning("⚠️ Please upload your resume first from the Resume Upload page.")
    st.stop()

resume_text = st.session_state["resume_text"]

def render_bot_bubble(text):
    st.markdown(
        '''
        <div style="
            padding: 12px 18px;
            background: #e6f0fc;
            border-radius: 18px 18px 18px 6px;
            max-width: 70%%;
            font-size: 16px;
            color: #222;
            margin: 14px 0 8px 0;
            box-shadow: 0 2px 6px #dde4ee;"
        >
            🧠 <b>Bot</b>: %s
        </div>
        ''' % text,
        unsafe_allow_html=True
    )

def render_bubbling_thinking():
    st.markdown(
        '''
        <style>
        @keyframes bounce {
            0%, 100% {
                transform: translateY(0);
            }
            20% {
                transform: translateY(-8px);
            }
            40% {
                transform: translateY(0);
            }
            60% {
                transform: translateY(-4px);
            }
            80% {
                transform: translateY(0);
            }
        }
        .bubble-bounce {
            animation: bounce 1.2s infinite;
            display: inline-block;
        }
        </style>
        <div class="bubble-bounce" style="
            padding: 12px 18px;
            background: #f0f2f6;
            border-radius: 18px 18px 18px 6px;
            max-width: 70%;
            font-size: 16px;
            color: #333;
            margin: 12px 0;
            font-style: italic;
            opacity: 0.7;
            display: inline-block;
        ">
            🧠 <b>Bot is thinking</b>
            <span style="opacity:0.4">. . .</span>
        </div>
        ''',
        unsafe_allow_html=True
    )


if st.button("🎙️ Start Interview"):
    st.success("Interview Started! 🎧 Say 'yes' to start")

    # ----- Greeting -----
    greeting = "Hello, I am your HR for today. I’ll be conducting your interview. Are you ready?"
    text_to_speech(greeting)
    question_placeholder = st.empty()
    question_placeholder.markdown("")  # Clear

    with question_placeholder.container():
        render_bot_bubble(greeting)

    confirmation = speech_to_text()

    if "yes" not in confirmation.lower():
        st.warning("Interview not started. Please restart and confirm readiness.")
    else:
        chat_history = []
        start_time = time.time()
        general_count = 0

        while True:
            elapsed = time.time() - start_time
            if elapsed > 15 * 60:
                question_placeholder.markdown(
                    '''<div style="color:#999;">⏰ Interview time (15 minutes) is over.</div>''',
                    unsafe_allow_html=True
                )
                break

            # ----- Show bubbling thinking -----
            bubble = st.empty()
            with bubble.container():
                render_bubbling_thinking()
            time.sleep(1.2)
            bubble.empty()
            # ---------------------------------

            # Category logic
            if general_count < 2:
                category = "general"
                general_count += 1
            else:
                category = "technical" if len(chat_history) % 2 == 0 else "projects"

            # ----- Ask question -----
            question = run_interview(resume_text, chat_history, category)

            with question_placeholder.container():
                render_bot_bubble(question)
            text_to_speech(question)

            # ----- Get user answer -----
            answer = speech_to_text()

            # ----- Listen for stop/quit -----
            if "quit" in answer.lower() or "stop" in answer.lower():
                question_placeholder.markdown(
                    '''<div style="color:#258a2a;font-weight:bold;">✅ Interview ended by user.</div>''',
                    unsafe_allow_html=True
                )
                break

            # ----- Handle empty or sorry -----
            if "sorry" in answer.lower() or not answer.strip():
                text_to_speech("Didn't catch that. Please repeat.")
                answer = speech_to_text()

                if "quit" in answer.lower() or "stop" in answer.lower():
                    question_placeholder.markdown(
                        '''<div style="color:#258a2a;font-weight:bold;">✅ Interview ended by user.</div>''',
                        unsafe_allow_html=True
                    )
                    break

            # ----- Store Q&A -----
            chat_history.append({"question": question, "answer": answer})

        # Store for feedback page
        st.session_state["chat_history"] = chat_history
        # Redirect to feedback
        st.success("✅ Interview complete!")
        st.session_state.redirected = True
        st.markdown("Redirecting to Feedback Page...")
        time.sleep(3)
        st.switch_page("pages/3_Feedback.py")
