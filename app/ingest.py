import re
from bisect import bisect_right
from pathlib import Path

from pgvector.psycopg import register_vector
from pypdf import PdfReader

from app.db import get_conn
from app.embeddings import embed_pasajes

TAMAÑO = 500
SOLAPE = 100

# ---------- Lectura y troceado ----------


def leer_pdf(ruta: Path) -> list[tuple[int, str]]:
    """Devuelve una lista de (número de página, texto) de un PDF."""
    lector = PdfReader(ruta)
    paginas = []
    for numero, pagina in enumerate(lector.pages, start=1):
        texto = (pagina.extract_text() or "").strip()
        if texto:
            paginas.append((numero, texto))
    return paginas


def limpiar(texto: str) -> str:
    """Quita saltos de línea y espacios repetidos."""
    return re.sub(r"\s+", " ", texto).strip()


def _trocear_con_inicio(texto: str, tamaño: int, solape: int) -> list[tuple[int, str]]:
    """Como `trocear`, pero devuelve (posición de inicio, trozo)."""
    if solape >= tamaño:
        raise ValueError("El solape debe ser menor que el tamaño")

    texto = limpiar(texto)
    trozos = []
    inicio = 0

    while inicio < len(texto):
        fin = min(inicio + tamaño, len(texto))

        # Cortar en el último espacio para no partir la palabra final
        if fin < len(texto):
            corte = texto.rfind(" ", inicio, fin)
            if corte > inicio + tamaño // 2:
                fin = corte

        bruto = texto[inicio:fin]
        trozo = bruto.strip()
        if trozo:
            desplazamiento = len(bruto) - len(bruto.lstrip())
            trozos.append((inicio + desplazamiento, trozo))
        if fin >= len(texto):
            break

        # El siguiente trozo empieza `solape` caracteres antes...
        siguiente = max(fin - solape, inicio + 1)
        # ...pero al principio de una palabra, no a mitad
        if texto[siguiente - 1] != " ":
            espacio = texto.find(" ", siguiente, fin)
            if espacio != -1:
                siguiente = espacio + 1
        inicio = siguiente

    return trozos


def trocear(texto: str, tamaño: int = TAMAÑO, solape: int = SOLAPE) -> list[str]:
    """Divide el texto en trozos de como máximo `tamaño` caracteres,
    con unos `solape` caracteres compartidos entre trozos consecutivos.
    No corta palabras."""
    return [t for _, t in _trocear_con_inicio(texto, tamaño, solape)]


def trocear_paginas(
    paginas: list[tuple[int, str]], tamaño: int = TAMAÑO, solape: int = SOLAPE
) -> list[tuple[int, str]]:
    """Trocea el documento entero, sin cortar las frases que cruzan un salto
    de página. Cada trozo lleva la página donde empieza."""
    partes = [(n, limpiar(t)) for n, t in paginas]
    partes = [(n, t) for n, t in partes if t]
    if not partes:
        return []

    texto = ""
    inicios = []
    for _, t in partes:
        if texto:
            texto += " "
        inicios.append(len(texto))
        texto += t

    numeros = [n for n, _ in partes]
    resultado = []
    for posicion, trozo in _trocear_con_inicio(texto, tamaño, solape):
        indice = bisect_right(inicios, posicion) - 1
        resultado.append((numeros[indice], trozo))
    return resultado


# ---------- Carga en base de datos ----------


def ingestar_pdf(conn, ruta: Path, tamaño: int = TAMAÑO, solape: int = SOLAPE) -> int:
    """Carga un PDF en la base de datos. Devuelve el número de fragmentos
    insertados (0 si el documento ya estaba cargado)."""
    fila = conn.execute(
        "INSERT INTO documentos (nombre) VALUES (%s) "
        "ON CONFLICT (nombre) DO NOTHING RETURNING id",
        (ruta.name,),
    ).fetchone()
    if fila is None:
        return 0
    documento_id = fila[0]

    registros = trocear_paginas(leer_pdf(ruta), tamaño, solape)

    vectores = embed_pasajes([t for _, t in registros])

    with conn.cursor() as cur:
        cur.executemany(
            "INSERT INTO fragmentos (documento_id, pagina, texto, embedding) "
            "VALUES (%s, %s, %s, %s)",
            [(documento_id, p, t, v) for (p, t), v in zip(registros, vectores)],
        )
    return len(registros)


def ingestar_carpeta(carpeta: Path = Path("data")) -> dict:
    """Carga todos los PDFs de una carpeta. Es idempotente:
    los documentos ya cargados se saltan."""
    resumen = {"documentos_nuevos": 0, "fragmentos_nuevos": 0}
    with get_conn() as conn:
        register_vector(conn)
        for ruta in sorted(carpeta.glob("*.pdf")):
            n = ingestar_pdf(conn, ruta)
            if n:
                resumen["documentos_nuevos"] += 1
                resumen["fragmentos_nuevos"] += n
                print(f"{ruta.name}: {n} fragmentos")
    return resumen


def vaciar() -> None:
    """Borra todos los documentos y fragmentos para volver a ingestar."""
    with get_conn() as conn:
        conn.execute("TRUNCATE fragmentos, documentos RESTART IDENTITY CASCADE")
