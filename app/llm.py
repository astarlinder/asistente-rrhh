import time

from anthropic import Anthropic
from google import genai
from groq import Groq

from app.config import settings


class LLMError(Exception):
    """Ningún proveedor ha podido responder."""


def _gemini(prompt: str, system: str | None) -> str:
    client = genai.Client(api_key=settings.gemini_api_key.get_secret_value())
    config = {"temperature": 0}
    if system:
        config["system_instruction"] = system
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
    # Los modelos gpt-oss razonan antes de responder; "low" gasta muchos menos tokens
    extra = {"reasoning_effort": "low"} if "gpt-oss" in settings.groq_model else {}
    resp = client.chat.completions.create(
        model=settings.groq_model,
        messages=messages,
        temperature=0,
        extra_body=extra,
    )
    return resp.choices[0].message.content


def _claude(prompt: str, system: str | None) -> str:
    client = Anthropic(api_key=settings.anthropic_api_key.get_secret_value())
    extra = {"system": system} if system else {}
    resp = client.messages.create(
        model=settings.anthropic_model,
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
        **extra,
    )
    return "".join(b.text for b in resp.content if b.type == "text")


PROVEEDORES = {"gemini": _gemini, "groq": _groq, "claude": _claude}


def responder(
    prompt: str,
    system: str | None = None,
    intentos: int = 2,
    proveedor: str | None = None,
) -> dict:
    """Pregunta a un proveedor.

    Con `proveedor` se usa solo ese, sin fallback. Sin él, se usa el configurado
    y, si falla, los demás gratuitos: Claude (de pago) nunca entra por fallback.
    """
    if proveedor:
        orden = [proveedor]
    else:
        orden = [settings.llm_provider] + [
            p for p in PROVEEDORES if p not in (settings.llm_provider, "claude")
        ]
    errores = []

    for nombre in orden:
        for intento in range(1, intentos + 1):
            try:
                texto = PROVEEDORES[nombre](prompt, system)
                return {"texto": texto, "proveedor": nombre}
            except Exception as e:  # noqa: BLE001 - cualquier fallo del proveedor activa el fallback
                errores.append(f"{nombre} intento {intento}: {str(e)[:200]}")
                if any(c in str(e) for c in ("401", "403", "429")):
                    break  # clave mala o cuota agotada: pasar al siguiente proveedor
                time.sleep(2 * intento)

    raise LLMError(" | ".join(errores))
