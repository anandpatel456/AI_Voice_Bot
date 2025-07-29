import speech_recognition as sr
import pyttsx3

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)  
    engine.say(text)
    engine.runAndWait()

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
