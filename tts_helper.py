from transformers import pipeline

# Load the TTS model
tts = pipeline("text-to-speech", model="ai4bharat/indic-parler-tts")

def generate_tts(text: str, language: str = "hi") -> str:
    """Convert story text to speech and save as a file."""
    audio = tts(text, language=language)

    # Save to static/ so it can be served
    audio_path = "static/story_narration.wav"
    with open(audio_path, "wb") as f:
        f.write(audio["wav"])
    
    return audio_path
