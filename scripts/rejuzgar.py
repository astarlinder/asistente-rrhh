"""Vuelve a juzgar respuestas ya generadas con otro juez, sin llamar al RAG.

Uso: uv run python -m scripts.rejuzgar [ruta.json]
Sin argumento usa eval/progreso.json si existe, o el detalle más reciente.
El juez es el que indique JUEZ_PROVIDER.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

from app.config import settings
from scripts.evaluar import PROGRESO, informe, juzgar


def elegir_ruta() -> Path:
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    if PROGRESO.exists():
        return PROGRESO
        return max(Path("eval").glob("detalle_*.json"))


def main() -> None:
    if not settings.juez_provider:
        raise SystemExit("Define JUEZ_PROVIDER (por ejemplo claude) para rejuzgar.")

    ruta = elegir_ruta()
    detalle = json.loads(ruta.read_text(encoding="utf-8"))
    print(
        f"Rejuzgando {len(detalle)} respuestas de {ruta} con «{settings.juez_provider}»\n"
    )

    nuevos = []
    distintos = []
    for d in detalle:
        nueva = juzgar(d["pregunta"], d["respuesta_esperada"], d["respuesta_obtenida"])
        if nueva != d["correcta"]:
            distintos.append((d, nueva))
        nuevos.append({**d, "correcta": nueva})

    print(
        f"Coinciden con el juez anterior: {len(detalle) - len(distintos)}/{len(detalle)}\n"
    )
    for d, nueva in distintos:
        antes = "OK" if d["correcta"] else "MAL"
        ahora = "OK" if nueva else "MAL"
        print(f"- {d['id']:02d} [{d['tipo']}] antes {antes}, ahora {ahora}")
        print(f"  esperada: {d['respuesta_esperada'][:200]}")
        print(f"  obtenida: {d['respuesta_obtenida'][:200]}\n")

    print(informe(nuevos))

    salida = Path(
        f"eval/rejuzgado_{settings.juez_provider}_{datetime.now():%Y%m%d_%H%M}.json"
    )
    salida.write_text(
        json.dumps(nuevos, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Guardado en {salida}")


if __name__ == "__main__":
    main()
