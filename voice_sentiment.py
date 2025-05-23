# voice_sentiment.py
import streamlit as st
import speech_recognition as sr
from textblob import TextBlob

def record_voice():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ Listening... please speak.")
        audio = r.listen(source, phrase_time_limit=5)
        try:
            text = r.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand your voice."
        except sr.RequestError:
            return "API error: Could not request results."

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.2:
        mood = "positive"
    elif polarity < -0.2:
        mood = "negative"
    else:
        mood = "neutral"
    return mood, polarity
