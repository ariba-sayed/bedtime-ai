import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

load_dotenv()

client = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY")
)

# Replace these with your actual ElevenLabs voice IDs
VOICE_IDS = {
    "🌙 Gentle storyteller": "YPRmL2oHPibcUwJtQnPM",
    "🧚 Magical fairy": "6j8uSqQkZH2WrWDVIiRB",
    "🐻 Warm bedtime voice": "plP9aw1rizYgjFfuvLQ7",
    "✨ Dreamy narrator": "L1QogKoobNwLy4IaMsyA",
}


def generate_narration(story, voice_name):
    voice_id = VOICE_IDS[voice_name]

    audio = client.text_to_speech.convert(
        text=story,
        voice_id=voice_id,
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128"
    )

    return b"".join(audio)