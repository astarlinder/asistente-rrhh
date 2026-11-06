"""Mide si los datos de la respuesta esperada llegan al LLM, sin gastar cupo.

Para cada pregunta busca los 10 mejores trozos y comprueba, para k = 3, 5, 8 y
10, si el documento esperado está entre ellos y si todas las cifras de la
respuesta esperada aparecen en sus trozos. No usa LLM: es gratis y determinista.
Las preguntas se buscan tal cual, sin reformular.
"""

import json
import re
from datetime import datetime
from pathlib import Path

from app.ingest import SOLAPE, TAMAÑO
from app.search import buscar

KS = (3, 5, 8, 10)
RUTA_PREGUNTAS = Path("eval/preguntas.json")
RUTA_INFORME = Path("eval/recuperacion.md")


def normalizar(texto: str) -> str:
    """Minúsculas y sin separador de miles: '1 300' y '1.300' pasan a '1300'."""
    texto = texto.lower().replace("\u00a0", " ").replace("\u202f", " ")
    return re.sub(r"(?<=\d)[ .](?=\d{3}(?!\d))", "", texto)


def cifras(texto: str) -> list[str]:
    return re.findall(r"(?<!\d)\d+(?:,\d+)?(?!\d)", normalizar(texto))


def cifras_necesarias(pregunta: str, esperada: str) -> list[str]:
    """Cifras de la respuesta esperada que no vienen ya en la pregunta."""
    en_pregunta = set(cifras(pregunta))
    vistas = []
    for c in cifras(esperada):
        if c not in en_pregunta and c not in vistas:
            vistas.append(c)
    return vistas


def pct(aciertos: int, total: int) -> str:
    return f"{100 * aciertos / total:.0f} %" if total else "-"


def main() -> None:
    preguntas = json.loads(RUTA_PREGUNTAS.read_text(encoding="utf-8"))
    filas = []

    for p in preguntas:
        esperado = p["documento_esperado"]
        if esperado is None:
            continue
        resultados = buscar(p["pregunta"], k=max(KS))
        necesarias = cifras_necesarias(p["pregunta"], p["respuesta_esperada"])

        primer_doc = None
        primer_datos = None
        presentes: set[str] = set()
        for rango, r in enumerate(resultados, start=1):
            if r.documento != esperado:
                continue
            if primer_doc is None:
                primer_doc = rango
            presentes |= set(cifras(r.texto))
            if (
                primer_datos is None
                and necesarias
                and all(c in presentes for c in necesarias)
            ):
                primer_datos = rango

        filas.append(
            {
                "id": p["id"],
                "tipo": p["tipo"],
                "pregunta": p["pregunta"],
                "necesarias": necesarias,
                "faltan": [c for c in necesarias if c not in presentes],
                "primer_doc": primer_doc,
                "primer_datos": primer_datos,
            }
        )

    ahora = datetime.now().strftime("%Y-%m-%d %H:%M")
    lineas = [
        f"## Recuperación {ahora}",
        "",
        (
            f"Trozos de {TAMAÑO} caracteres (solape {SOLAPE}); "
            "búsqueda con la pregunta tal cual, sin reformular."
        ),
        "Documento esperado entre los k primeros trozos:",
        "",
        "| Tipo | Preguntas | " + " | ".join(f"@{k}" for k in KS) + " |",
        "| --- | --- | " + " | ".join("---" for _ in KS) + " |",
    ]
    for tipo in ("normal", "coloquial"):
        grupo = [f for f in filas if f["tipo"] == tipo]
        celdas = [
            pct(
                sum(1 for f in grupo if f["primer_doc"] and f["primer_doc"] <= k),
                len(grupo),
            )
            for k in KS
        ]
        lineas.append(f"| {tipo} | {len(grupo)} | " + " | ".join(celdas) + " |")

    lineas += [
        "",
        (
            "Todas las cifras de la respuesta esperada presentes en los trozos del "
            "documento esperado:"
        ),
        "",
        "| Tipo | Preguntas medibles | " + " | ".join(f"@{k}" for k in KS) + " |",
        "| --- | --- | " + " | ".join("---" for _ in KS) + " |",
    ]
    for tipo in ("normal", "coloquial"):
        grupo = [f for f in filas if f["tipo"] == tipo and f["necesarias"]]
        celdas = [
            pct(
                sum(1 for f in grupo if f["primer_datos"] and f["primer_datos"] <= k),
                len(grupo),
            )
            for k in KS
        ]
        lineas.append(f"| {tipo} | {len(grupo)} | " + " | ".join(celdas) + " |")

    sin_datos = [
        f
        for f in filas
        if f["necesarias"] and (f["primer_datos"] is None or f["primer_datos"] > 5)
    ]
    lineas += ["", "Sin todas las cifras en el top 5:"]
    for f in sin_datos:
        cuando = f["primer_datos"] or ">10"
        lineas.append(
            f"- {f['id']:02d} [{f['tipo']}] {f['pregunta'][:60]} "
            f"→ faltan {f['faltan']}; completo en k = {cuando}"
        )
    lineas.append("")

    informe = "\n".join(lineas)
    print(informe)
    with RUTA_INFORME.open("a", encoding="utf-8") as fh:
        fh.write(informe + "\n")


if __name__ == "__main__":
    main()
