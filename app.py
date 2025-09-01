import os
import webbrowser
import streamlit as st
from streamlit_audiorecorder import audiorecorder
import openai
import pyttsx3
import tempfile
import time

# ------------------------------
# Streamlit page config
# ------------------------------
st.set_page_config(page_title="Voice Assistant", page_icon="🎙️", layout="centered")

st.title("🎙️ Voice Assistant with Streamlit")

# Detect if running on Streamlit Cloud
IS_CLOUD = os.environ.get("STREAMLIT_SERVER_PORT") is not None

# ------------------------------
# Helper functions
# ------------------------------

def open_site(name, url):
    """Open a website depending on environment (local vs cloud)."""
    if IS_CLOUD:
        st.write(f"🔗 [Click here to open {name}]({url})")
    else:
        webbrowser.open(url)
        st.write(f"✅ Opened {name}")

def speak_text(text):
    """Convert text to speech locally with pyttsx3."""
    if IS_CLOUD:
        # No local audio playback on cloud, just show text
        st.info("🔊 TTS not available in Streamlit Cloud. Showing text instead.")
    else:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

def get_ai_response(user_text):
    """Call OpenAI API for chatbot response."""
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        return "⚠️ Missing OpenAI API Key. Set OPENAI_API_KEY env variable."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_text}]
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# ------------------------------
# Audio input
# ------------------------------
st.subheader("🎤 Record your voice")

audio = audiorecorder("Start Recording", "Stop Recording")

user_text = ""
if len(audio) > 0:
    # save audio temp
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        f.write(audio.tobytes())
        audio_path = f.name
    st.audio(audio_path, format="audio/wav")

    # (Optional) integrate speech-to-text here if you want
    user_text = st.text_input("Or type your command here 👇", "")

else:
    user_text = st.text_input("Type your command 👇", "")

# ------------------------------
# Process input
# ------------------------------
if st.button("Send") and user_text.strip() != "":
    text = user_text.lower()

    if "youtube" in text:
        open_site("YouTube", "https://www.youtube.com")
        reply = "Opening YouTube"
    elif "google" in text:
        open_site("Google", "https://www.google.com")
        reply = "Opening Google"
    elif "gmail" in text:
        open_site("Gmail", "https://mail.google.com")
        reply = "Opening Gmail"
    elif "instagram" in text:
        open_site("Instagram", "https://www.instagram.com")
        reply = "Opening Instagram"
    else:
        reply = get_ai_response(user_text)

    st.success(reply)
    speak_text(reply)
