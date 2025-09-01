import streamlit as st
from audiorecorder import audiorecorder
import speech_recognition as sr
import webbrowser
from gtts import gTTS
import os
import tempfile

st.title("🎤 Voice Assistant")

# Record audio using streamlit-audiorecorder
audio = audiorecorder("Click to record", "Recording...")

if len(audio) > 0:
    st.audio(audio.export().read(), format="audio/wav")

    # Save to temp wav file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
        audio.export(temp_wav.name, format="wav")
        temp_path = temp_wav.name

    # Recognize speech
    recognizer = sr.Recognizer()
    with sr.AudioFile(temp_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            st.write("You said:", text)

            # Actions
            if "YouTube" in text:
                st.write("🔗 Opening YouTube...")
                webbrowser.open("https://www.youtube.com")
            elif "Google" in text:
                st.write("🔗 Opening Google...")
                webbrowser.open("https://www.google.com")
            elif "Instagram" in text:
                st.write("🔗 Opening Instagram...")
                webbrowser.open("https://www.instagram.com")
            else:
                st.write("⚠️ Command not recognized.")

            # Voice reply
            tts = gTTS(text="Okay, " + text)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_mp3:
                tts.save(temp_mp3.name)
                st.audio(temp_mp3.name, format="audio/mp3")

        except sr.UnknownValueError:
            st.error("Sorry, could not understand audio.")
        except sr.RequestError:
            st.error("Could not request results, check internet connection.")
