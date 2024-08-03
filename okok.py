import speech_recognition as sr
import streamlit as st

# Initialize recognizer
recognizer = sr.Recognizer()

# Function to capture and recognize speech
def recognize_speech():
    with sr.Microphone() as source:
        st.write("Listening... Please speak clearly.")
        audio = recognizer.listen(source)

        try:
            # Recognize speech using Google Web Speech API
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I could not understand the audio."
        except sr.RequestError:
            return "Could not request results; check your network connection."

# Streamlit UI setup
st.title("Speech-to-Text with Streamlit")
st.write("Click the button below and start speaking.")

if st.button('Click here to record'):
    st.write("Recording...")
    result = recognize_speech()
    st.write("You said: ", result)

    