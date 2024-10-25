import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# For parsing
PARSING_API_URL = os.getenv("PARSING_API_URL", "https://api.deepinfra.com/v1/openai")
PARSING_API_KEY = os.environ["DEEPINFRA_API_KEY"]

# For transcription
TRANSCRIPTION_API_URL = os.getenv("TRANSCRIPTION_API_URL", "https://api.lemonfox.ai/v1/audio/transcriptions")
TRANSCRIPTION_API_KEY = os.environ["LEMONFOX_API_KEY"]

