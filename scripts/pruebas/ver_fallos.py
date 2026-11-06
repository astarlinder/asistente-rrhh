"""Muestra en detalle los fallos de la última evaluación."""

import json
from pathlib import Path

ultimo = max(Path("eval").glob("detalle_*.json"))
detalle = json.loads(ultimo.read_text(encoding="utf-8"))
print(f"Archivo: {ultimo.name}\n")

for d in detalle:
    if d["correcta"]:
        continue
    print("=" * 80)
    print(f"{d['id']:02d} [{d['tipo']}] {d['pregunta']}")
    print(f"\nDOC ESPERADO:  {d['documento_esperado']} (pág. {d['pagina_esperada']})")
    print(f"DOCS OBTENIDOS: {d['documentos_recuperados']}")
    print(f"\nESPERADA:  {d['respuesta_esperada']}")
    print(f"OBTENIDA:  {d['respuesta_obtenida']}\n")
