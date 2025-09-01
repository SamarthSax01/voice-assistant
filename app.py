import streamlit as st
import speech_recognition as sr
import webbrowser
from gtts import gTTS
import os
import datetime
import random
from audiorecorder import audiorecorder

st.title("🎤 Smart Voice Assistant")
st.write("Say a command and I will respond...")

recognizer = sr.Recognizer()

# Function to speak
def speak(text):
    tts = gTTS(text)
    tts.save("reply.mp3")
    st.audio("reply.mp3", format="audio/mp3")

# Handle commands
def process_command(text):
    if "youtube" in text:
        st.write("Opening YouTube...")
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube")

    elif "google" in text:
        st.write("Opening Google...")
        webbrowser.open("https://google.com")
        speak("Opening Google")

    elif "gmail" in text:
        st.write("Opening Gmail...")
        webbrowser.open("https://mail.google.com")
        speak("Opening Gmail")

    elif "time" in text:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        st.write(f"The time is {current_time}")
        speak(f"The time is {current_time}")

    elif "hello" in text or "hi" in text:
        reply = "Hello! How can I help you today?"
        st.write(reply)
        speak(reply)

    elif "joke" in text:
        jokes = [
            "Why don’t scientists trust atoms? Because they make up everything!",
            "I told my computer a joke, but it didn’t laugh. Too many bytes!",
            "Why was the math book sad? Because it had too many problems."
        ]
        joke = random.choice(jokes)
        st.write(joke)
        speak(joke)

    elif text:
        reply = f"You said {text}"
        st.write(reply)
        speak(reply)

# Audio recorder widget
audio = audiorecorder("🎙️ Start recording", "⏹️ Stop recording")

if len(audio) > 0:
    st.audio(audio.export().read(), format="audio/wav")

    # Save recorded audio
    audio.export("input.wav", format="wav")

    with sr.AudioFile("input.wav") as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            st.write(f"You said: {text}")
            process_command(text.lower())
        except:
            st.write("Sorry, I couldn't understand.")
