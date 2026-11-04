"""Genera una pregunta de evaluación por documento usando la IA."""

import json
from pathlib import Path

from app.ingest import leer_pdf
from app.llm import responder

SYSTEM = """Eres un empleado de un hotel que pregunta a RR. HH.
A partir del documento, escribe UNA pregunta que haría un empleado real y su respuesta.

Reglas:
- La pregunta debe sonar natural y NO copiar las palabras del documento
  (ej.: "¿cuánto cobro si trabajo de noche?" en vez de "¿cuál es el plus de nocturnidad?").
- La respuesta debe estar literalmente en el documento e incluir la cifra o dato concreto.
- Devuelve SOLO un JSON válido, sin texto adicional ni ```:
{"pregunta": "...", "respuesta_esperada": "...", "pagina": 1}"""


def extraer_json(texto: str) -> dict:
    """La IA a veces añade ``` o texto alrededor: nos quedamos con el JSON."""
    inicio, fin = texto.find("{"), texto.rfind("}")
    return json.loads(texto[inicio : fin + 1])


preguntas = []
for i, ruta in enumerate(sorted(Path("data").glob("*.pdf")), start=1):
    contenido = "\n\n".join(f"[Página {p}]\n{t}" for p, t in leer_pdf(ruta))
    r = responder(f"DOCUMENTO: {ruta.name}\n\n{contenido}", system=SYSTEM)
    datos = extraer_json(r["texto"])
    preguntas.append(
        {
            "id": i,
            "tipo": "normal",
            "pregunta": datos["pregunta"],
            "documento_esperado": ruta.name,
            "pagina_esperada": datos.get("pagina", 1),
            "respuesta_esperada": datos["respuesta_esperada"],
        }
    )
    print(f"{i:02d}. {datos['pregunta']}")

Path("eval/preguntas.json").write_text(
    json.dumps(preguntas, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(f"\nGuardadas {len(preguntas)} preguntas en eval/preguntas.json")