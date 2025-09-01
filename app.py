import streamlit as st
from streamlit_audiorecorder import audiorecorder
import openai
import pyttsx3
import tempfile
import os
import webbrowser

# Set your OpenAI API key (use Streamlit secrets in real deploy)
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("🎤 Voice Assistant with Streamlit")

# Record audio
audio = audiorecorder("Click to record", "Recording...")

if len(audio) > 0:
    # Save temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
        audio.export(tmpfile.name, format="wav")
        audio_path = tmpfile.name

    st.audio(audio_path, format="audio/wav")

    # ---- Speech to Text ----
    with open(audio_path, "rb") as f:
        transcript = openai.Audio.transcriptions.create(
            model="gpt-4o-transcribe", 
            file=f
        )
    user_text = transcript.text
    st.write("🗣️ You said:", user_text)

    # ---- ChatGPT response ----
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_text}]
    )
    answer = response.choices[0].message.content
    st.write("🤖 Assistant:", answer)

    # ---- Text to Speech ----
    engine = pyttsx3.init()
    engine.save_to_file(answer, "response.mp3")
    engine.runAndWait()
    st.audio("response.mp3", format="audio/mp3")

    # ---- Example Action ----
    if "youtube" in user_text.lower():
        st.write("🔗 Opening YouTube...")
        webbrowser.open("https://www.youtube.com")
