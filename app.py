import streamlit as st
from audiorecorder import audiorecorder
import speech_recognition as sr
from gtts import gTTS
import os
from pydub import AudioSegment

st.title("🎤 Samarth's Voice Assistant")
st.write("Talk to me, and I'll reply!")

recognizer = sr.Recognizer()

def recognize_audio(audio_bytes):
    """Convert recorded audio (bytes) into text"""
    with open("input.wav", "wb") as f:
        f.write(audio_bytes)

    # Convert to wav format
    audio = AudioSegment.from_file("input.wav")
    audio.export("converted.wav", format="wav")

    with sr.AudioFile("converted.wav") as source:
        recorded_audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(recorded_audio)
            return text
        except:
            return ""

# Record audio in Streamlit
audio = audiorecorder("🎙️ Click to Record", "🔴 Recording...")

if len(audio) > 0:
    # Save recording
    audio.export("recorded.wav", format="wav")
    st.audio("recorded.wav", format="audio/wav")

    # Recognize speech
    text = recognize_audio(audio.export().read())
    if text:
        st.write(f"You said: **{text}**")

        response = None
        link = None

        if "youtube" in text.lower():
            response = "✅ Opening YouTube..."
            link = "https://youtube.com"
        elif "google" in text.lower():
            response = "✅ Opening Google..."
            link = "https://www.google.com"
        elif "whatsapp" in text.lower():
            response = "✅ Opening WhatsApp Web..."
            link = "https://web.whatsapp.com"
        elif "instagram" in text.lower() or "insta" in text.lower():
            response = "✅ Opening Instagram..."
            link = "https://www.instagram.com"

        if response:
            st.success(response)
            st.markdown(f"[Click here to open]({link})", unsafe_allow_html=True)

        # Generate voice reply
        reply = f"You said {text}"
        tts = gTTS(reply)
        tts.save("reply.mp3")
        st.audio("reply.mp3", format="audio/mp3")
    else:
        st.warning("⚠️ Sorry, I couldn’t understand your speech.")
