import time

from google import genai
from groq import Groq

from app.config import settings


class LLMError(Exception):
    """Ningún proveedor ha podido responder."""


def _gemini(prompt: str, system: str | None) -> str:
    client = genai.Client(api_key=settings.gemini_api_key.get_secret_value())
    config = {"system_instruction": system} if system else None
    resp = client.models.generate_content(
        model=settings.gemini_model, contents=prompt, config=config
    )
    return resp.text


def _groq(prompt: str, system: str | None) -> str:
    client = Groq(api_key=settings.groq_api_key.get_secret_value())
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    resp = client.chat.completions.create(model=settings.groq_model, messages=messages)
    return resp.choices[0].message.content


PROVEEDORES = {"gemini": _gemini, "groq": _groq}


def responder(prompt: str, system: str | None = None, intentos: int = 2) -> dict:
    """Pregunta al proveedor configurado; si falla, prueba con los demás."""
    orden = [settings.llm_provider] + [p for p in PROVEEDORES if p != settings.llm_provider]
    errores = []

    for proveedor in orden:
        for intento in range(1, intentos + 1):
            try:
                texto = PROVEEDORES[proveedor](prompt, system)
                return {"texto": texto, "proveedor": proveedor}
            except Exception as e:
                errores.append(f"{proveedor} intento {intento}: {str(e)[:200]}")
                if any(c in str(e) for c in ("401", "403", "429")):
                    break  # clave mala o cuota agotada: pasar al siguiente proveedor
                time.sleep(2 * intento)

    raise LLMError(" | ".join(errores))