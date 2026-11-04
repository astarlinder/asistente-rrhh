from pathlib import Path

from app.ingest import leer_pdf

total_paginas = 0
for ruta in sorted(Path("data").glob("*.pdf")):
    paginas = leer_pdf(ruta)
    caracteres = sum(len(t) for _, t in paginas)
    total_paginas += len(paginas)
    aviso = "  <-- REVISAR" if caracteres < 1500 else ""
    print(f"{ruta.name:60} {len(paginas)} pág. {caracteres:6} car.{aviso}")

print(f"\nTotal: {total_paginas} páginas")

# Muestra el principio del primer PDF para comprobar tildes y eñes
primero = min(Path("data").glob("*.pdf"))
print(f"\n--- Muestra de {primero.name}, página 1 ---")
print(leer_pdf(primero)[0][1][:400])
