import requests

from config import TRANSCRIPTION_API_URL, TRANSCRIPTION_API_KEY

TRANSCRIPTION_DATA = {
    "response_format": "json",
    "language": "french",
    "prompt": ("Ce transcript il s'agit d'une requête de recherche des profils IT contenant leurs compétences, "
               "les langues, la disponibilité et le niveau d'étude. Les profils sont basés sur le Maroc.")
}


class Transcribe:
    """Transcription"""

    @staticmethod
    def transcribe(audio_file):
        headers = {
            "Authorization": f"Bearer {TRANSCRIPTION_API_KEY}"
        }
        files = {
            "file": ("test.wav", audio_file, "audio/wav"),
        }
        return requests.post(TRANSCRIPTION_API_URL, headers=headers, data=TRANSCRIPTION_DATA, files=files)
