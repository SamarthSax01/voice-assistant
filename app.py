import streamlit as st
import speech_recognition as sr
import webbrowser
from gtts import gTTS
import os
import datetime
import random

st.title("🎤 Smart Voice Assistant")
st.write("Say a command and I will respond...")

recognizer = sr.Recognizer()

# Function to listen
def listen():
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            st.write(f"You said: {command}")
            return command.lower()
        except:
            st.write("Sorry, I couldn't understand.")
            return ""

# Function to speak
def speak(text):
    tts = gTTS(text)
    tts.save("reply.mp3")
    os.system("start reply.mp3")

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

# Button to activate mic
if st.button("🎙️ Speak"):
    text = listen()
    if text:
        process_command(text)
