"""Evalúa el RAG con eval/preguntas.json y guarda los resultados."""

import json
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from app.config import settings
from app.llm import responder
from app.rag import preguntar

JUEZ = """Eres un evaluador estricto de un asistente de RR. HH.
Compara la RESPUESTA DEL SISTEMA con la RESPUESTA ESPERADA.
Es CORRECTA si contiene los datos clave de la esperada (cifras, plazos, responsables)
y no contradice nada. Puede añadir información extra si no es falsa.
Contesta SOLO con una palabra: CORRECTA o INCORRECTA."""


def juzgar(pregunta: str, esperada: str, obtenida: str) -> bool:
    dice_no_aparece = "no aparece" in obtenida.lower()
    # Preguntas trampa: lo correcto es decir que no aparece
    if esperada.lower().startswith("no aparece"):
        return dice_no_aparece
    # Pregunta con respuesta pero el sistema dice que no aparece: fallo
    if dice_no_aparece:
        return False
    r = responder(
        f"PREGUNTA: {pregunta}\n"
        f"RESPUESTA ESPERADA: {esperada}\n"
        f"RESPUESTA DEL SISTEMA: {obtenida}",
        system=JUEZ,
    )
    veredicto = r["texto"].strip().upper()
    return "INCORRECTA" not in veredicto and "CORRECTA" in veredicto


def porcentaje(n: int, total: int) -> str:
    return f"{100 * n / total:.0f} %" if total else "-"


def main() -> None:
    preguntas = json.loads(Path("eval/preguntas.json").read_text(encoding="utf-8"))
    detalle = []

    for p in preguntas:
        inicio = time.perf_counter()
        r = preguntar(p["pregunta"])
        segundos = time.perf_counter() - inicio

        documentos = [f.documento for f in r.fuentes]
        esperado = p["documento_esperado"]
        correcta = juzgar(p["pregunta"], p["respuesta_esperada"], r.respuesta)

        detalle.append(
            {
                **p,
                "respuesta_obtenida": r.respuesta,
                "proveedor": r.proveedor,
                "documentos_recuperados": documentos,
                "recuperacion_1": bool(esperado) and documentos[:1] == [esperado],
                "recuperacion_5": bool(esperado) and esperado in documentos,
                "correcta": correcta,
                "segundos": round(segundos, 2),
            }
        )
        marca = "OK " if correcta else "MAL"
        print(f"{marca} {p['id']:02d} [{p['tipo']}] {p['pregunta'][:70]}")
        time.sleep(1)  # respetar los límites del plan gratis

    # ---------- Resumen por tipo ----------
    grupos = defaultdict(list)
    for d in detalle:
        grupos[d["tipo"]].append(d)
    grupos["TOTAL"] = detalle

    filas = []
    for tipo, items in grupos.items():
        con_doc = [d for d in items if d["documento_esperado"]]
        filas.append(
            f"| {tipo} | {len(items)} "
            f"| {porcentaje(sum(d['recuperacion_1'] for d in con_doc), len(con_doc))} "
            f"| {porcentaje(sum(d['recuperacion_5'] for d in con_doc), len(con_doc))} "
            f"| {porcentaje(sum(d['correcta'] for d in items), len(items))} |"
        )

    sin_llamada = sum(d["proveedor"] == "ninguno" for d in detalle)
    tiempo_medio = sum(d["segundos"] for d in detalle) / len(detalle)
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M")

    informe = (
        f"\n## Evaluación {ahora}\n\n"
        f"Configuración: proveedor `{settings.llm_provider}`, k = 5, "
        f"trozos de 800 caracteres, umbral {settings.umbral_similitud}\n\n"
        "| Tipo | Preguntas | Recuperación @1 | Recuperación @5 | Respuesta correcta |\n"
        "| --- | --- | --- | --- | --- |\n"
        + "\n".join(filas)
        + f"\n\nTiempo medio por pregunta: {tiempo_medio:.1f} s · "
        f"Preguntas cortadas por el umbral (sin llamar a la IA): {sin_llamada}\n"
    )

    fallos = [d for d in detalle if not d["correcta"]]
    if fallos:
        informe += "\nFallos:\n" + "\n".join(
            f"- {d['id']:02d} [{d['tipo']}] {d['pregunta']} → recuperó "
            f"{d['documentos_recuperados'][:1] or 'nada'}"
            for d in fallos
        ) + "\n"

    with open("eval/resultados.md", "a", encoding="utf-8") as f:
        f.write(informe)

    sello = datetime.now().strftime("%Y%m%d_%H%M")
    Path(f"eval/detalle_{sello}.json").write_text(
        json.dumps(detalle, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(informe)


if __name__ == "__main__":
    main()