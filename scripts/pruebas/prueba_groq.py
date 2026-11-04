import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

respuesta = client.chat.completions.create(
    model=os.getenv("GROQ_MODEL"),
    messages=[{"role": "user", "content": "Hola, preséntate en una frase."}],
)

print(respuesta.choices[0].message.content)
print("Tokens usados:", respuesta.usage.total_tokens)
