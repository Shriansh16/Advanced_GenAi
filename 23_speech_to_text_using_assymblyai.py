import assemblyai as aai

aai.settings.api_key = "551dfcff51044bddb82c8cb562046329"

# Audio file path
audio_file = "meeting_with_neighbour.wav"

# Create config with speaker diarization enabled
config = aai.TranscriptionConfig(speaker_labels=True)

# Transcribe with speaker labels
transcriber = aai.Transcriber()
transcript = transcriber.transcribe(audio_file, config=config)

# Print structured transcript
for utterance in transcript.utterances:
    print(f"Speaker {utterance.speaker} [{utterance.start / 1000:.2f}s - {utterance.end / 1000:.2f}s]: {utterance.text}")
