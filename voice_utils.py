import speech_recognition as sr
from gtts import gTTS
from io import BytesIO
import base64
import streamlit as st
import time

def estimate_speech_duration(text, wpm=180, speed=1.25):
    """Estimate how long the TTS will take to speak, based on word count and speed."""
    words = len(text.split())
    return (words / wpm) * 60 / speed  # seconds

def text_to_speech(text, lang="en", speed=1.50):
    """Speak text using gTTS and wait until it's done before moving on"""
    tts = gTTS(text=text, lang=lang)
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    audio_data = mp3_fp.read()

    b64 = base64.b64encode(audio_data).decode()
    audio_html = f"""
        <audio id="tts-audio" autoplay>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        <script>
            var audio = document.getElementById("tts-audio");
            audio.playbackRate = {speed};
        </script>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

    # Wait until the audio finishes (estimated duration)
    est_duration = estimate_speech_duration(text, speed=speed)
    time.sleep(est_duration + 0.5)


def speech_to_text(timeout=10, phrase_time_limit=60, pause_threshold=1.5):
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = pause_threshold  # Allow longer pauses
    with sr.Microphone() as source:
        print("Adjusting for background noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening... (you can pause briefly while speaking)")
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            print("Transcribing...")
            text = recognizer.recognize_google(audio)
            return text
        except sr.WaitTimeoutError:
            return "Sorry, you didn't respond in time."
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand that. Please try again."
        except sr.RequestError as e:
            return f"Speech recognition error: {e}"
