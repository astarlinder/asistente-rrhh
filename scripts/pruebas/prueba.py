import os

from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

modelos = [
    os.getenv("GEMINI_MODEL"),
    "gemini-flash-latest",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
]

for modelo in modelos:
    print(f"Probando {modelo}...")
    try:
        respuesta = client.models.generate_content(
            model=modelo,
            contents="Hola, preséntate en una frase.",
        )
        print("OK ->", respuesta.text)
        print("Tokens usados:", respuesta.usage_metadata.total_token_count)
        break
    except errors.APIError as e:
        print(f"  Falla ({e.code}): {e.message}")
