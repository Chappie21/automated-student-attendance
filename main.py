from model.geminiAdapter import GeminiAdapter
from dotenv import load_dotenv
import os


load_dotenv()

try:
    client = GeminiAdapter(
        api_key=os.getenv("GEMINI_API_KEY"),
        model=os.getenv("GEMINI_MODEL")
    )

    response = client.generate_text(prompt="Hola, qué versión eres?")
    print(response)
except Exception as e:
    print(f"Connection error: {e}")