import streamlit as st
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
import speech_recognition as sr
import numpy as np

recognizer = sr.Recognizer()

class SpeechRecognizer(AudioProcessorBase):
    def __init__(self):
        self.text = ""

    def recv(self, frame):
        audio_data = np.frombuffer(frame.to_ndarray().tobytes(), np.int16)
        audio = sr.AudioData(audio_data.tobytes(), 16000, 2)
        try:
            self.text = recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            self.text = "Sorry, I couldn't understand the audio."
        except sr.RequestError:
            self.text = "Sorry, there was an issue with the speech recognition service."
        return frame

def recognize_speech():
    webrtc_ctx = webrtc_streamer(
        key="speech-recognizer", 
        audio_processor_factory=SpeechRecognizer,
        desired_playing_state=True,
    )

    if webrtc_ctx.state.playing:
        if webrtc_ctx.audio_processor:
            # Wait until the user speaks and audio is processed
            while not webrtc_ctx.audio_processor.text:
                pass
            return webrtc_ctx.audio_processor.text
    else:
        return "WebRTC not started or no audio input detected."