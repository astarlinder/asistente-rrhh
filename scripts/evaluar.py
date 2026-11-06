"""Evalúa el RAG con eval/preguntas.json y guarda los resultados.
Se puede reanudar: si se corta, al relanzarlo salta las preguntas ya hechas."""

import json
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from app.config import settings
from app.ingest import TAMAÑO
from app.llm import responder
from app.rag import preguntar

PROGRESO = Path("eval/progreso.json")

JUEZ = """Eres un evaluador de un asistente de RR. HH.
Decide si la RESPUESTA DEL SISTEMA responde correctamente a la PREGUNTA,
usando la RESPUESTA ESPERADA como referencia.

Es CORRECTA si:
- contiene el dato que responde a la pregunta (cifra, plazo o responsable) y coincide con la esperada;
- puede omitir detalles secundarios de la esperada que la pregunta no pide;
- puede añadir información extra si no contradice la esperada.

Es INCORRECTA si:
- el dato principal no coincide (otra cifra, otro plazo, otro responsable);
- no responde a lo que se pregunta.

Contesta SOLO con una palabra: CORRECTA o INCORRECTA."""


def juzgar(pregunta: str, esperada: str, obtenida: str) -> bool:
    dice_no_aparece = "no aparece" in obtenida.lower()
    # Preguntas trampa: lo correcto es decir que no aparece
    if esperada.lower().startswith("no aparece"):
        return dice_no_aparece
    # Había respuesta pero el sistema dice que no aparece: fallo
    if dice_no_aparece:
        return False
    r = responder(
        f"PREGUNTA: {pregunta}\n"
        f"RESPUESTA ESPERADA: {esperada}\n"
        f"RESPUESTA DEL SISTEMA: {obtenida}",
        system=JUEZ,
        proveedor=settings.juez_provider,
    )
    veredicto = r["texto"].strip().upper()
    return "INCORRECTA" not in veredicto and "CORRECTA" in veredicto


def porcentaje(n: int, total: int) -> str:
    return f"{100 * n / total:.0f} %" if total else "-"


def evaluar_pregunta(p: dict) -> dict:
    inicio = time.perf_counter()
    r = preguntar(p["pregunta"])
    segundos = time.perf_counter() - inicio
    documentos = [f.documento for f in r.fuentes]
    esperado = p["documento_esperado"]
    return {
        **p,
        "respuesta_obtenida": r.respuesta,
        "consulta_reformulada": r.consulta,
        "proveedor": r.proveedor,
        "citas_invalidas": r.citas_invalidas,
        "documentos_recuperados": documentos,
        "recuperacion_1": bool(esperado) and documentos[:1] == [esperado],
        "recuperacion_5": bool(esperado) and esperado in documentos,
        "correcta": juzgar(p["pregunta"], p["respuesta_esperada"], r.respuesta),
        "segundos": round(segundos, 2),
    }


def informe(detalle: list[dict]) -> str:
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
    medidas = [d for d in detalle if "citas_invalidas" in d]
    con_citas_malas = sum(bool(d["citas_invalidas"]) for d in medidas)
    texto = (
        f"\n## Evaluación {datetime.now():%Y-%m-%d %H:%M}\n\n"
        f"Configuración: `{settings.llm_provider}` / `{settings.groq_model}`, k = 5, "
        f"trozos de {TAMAÑO} caracteres, umbral {settings.umbral_similitud}, "
        f"reformular {settings.reformular}\n\n"
        "| Tipo | Preguntas | Recuperación @1 | Recuperación @5 | Respuesta correcta |\n"
        "| --- | --- | --- | --- | --- |\n"
        + "\n".join(filas)
        + f"\n\nTiempo medio por pregunta: {tiempo_medio:.1f} s · "
        f"Preguntas cortadas por el umbral: {sin_llamada}\n"
        f"Respuestas con citas inválidas: {con_citas_malas} de {len(medidas)} medidas\n"
    )
    fallos = [d for d in detalle if not d["correcta"]]
    if fallos:
        lineas = []
        for d in fallos:
            linea = (
                f"- {d['id']:02d} [{d['tipo']}] {d['pregunta']} → recuperó "
                f"{d['documentos_recuperados'][:1] or 'nada'}"
            )
            if d.get("consulta_reformulada"):
                linea += f" (consulta: «{d['consulta_reformulada']}»)"
            if d.get("citas_invalidas"):
                linea += f" [citas inválidas: {d['citas_invalidas']}]"
            lineas.append(linea)
        texto += "\nFallos:\n" + "\n".join(lineas) + "\n"
    return texto


def main() -> None:
    preguntas = json.loads(Path("eval/preguntas.json").read_text(encoding="utf-8"))
    detalle = (
        json.loads(PROGRESO.read_text(encoding="utf-8")) if PROGRESO.exists() else []
    )
    hechas = {d["id"] for d in detalle}
    if hechas:
        print(f"Reanudando: {len(hechas)} preguntas ya evaluadas")

    for p in preguntas:
        if p["id"] in hechas:
            continue
        d = evaluar_pregunta(p)
        detalle.append(d)
        PROGRESO.write_text(
            json.dumps(detalle, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        marca = "OK " if d["correcta"] else "MAL"
        print(f"{marca} {p['id']:02d} [{p['tipo']}] {p['pregunta'][:70]}")
        time.sleep(2)  # respetar los límites del plan gratis

    texto = informe(detalle)
    with open("eval/resultados.md", "a", encoding="utf-8") as f:
        f.write(texto)
    Path(f"eval/detalle_{datetime.now():%Y%m%d_%H%M}.json").write_text(
        json.dumps(detalle, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    PROGRESO.unlink()
    print(texto)


if __name__ == "__main__":
    main()
