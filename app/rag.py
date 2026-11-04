from app.llm import responder
from app.schemas import Fuente, Respuesta
from app.search import buscar

SYSTEM = """Eres el asistente de RR. HH. de Hoteles Tramuntana.
Responde a la pregunta del empleado usando EXCLUSIVAMENTE las fuentes proporcionadas.

Reglas:
- Si la respuesta está en las fuentes, contesta de forma breve y concreta (máximo 4 frases), con las cifras exactas.
- Después de cada dato, cita la fuente así: (nombre_del_documento.pdf, pág. N).
- Si las fuentes no contienen la respuesta, responde exactamente: "No aparece en la documentación de RR. HH."
- No inventes nada ni uses conocimiento general sobre leyes o empresas.
- Responde en español y tutea al empleado."""


def construir_contexto(fuentes: list[Fuente]) -> str:
    bloques = [
        f"[Fuente {i}] {f.documento}, pág. {f.pagina}\n{f.texto}"
        for i, f in enumerate(fuentes, start=1)
    ]
    return "\n\n".join(bloques)


def preguntar(pregunta: str, k: int = 5) -> Respuesta:
    fuentes = buscar(pregunta, k)
    prompt = f"FUENTES:\n\n{construir_contexto(fuentes)}\n\nPREGUNTA: {pregunta}"
    r = responder(prompt, system=SYSTEM)
    return Respuesta(respuesta=r["texto"], proveedor=r["proveedor"], fuentes=fuentes)