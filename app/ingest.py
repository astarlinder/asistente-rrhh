import re
from pathlib import Path

from pgvector.psycopg import register_vector
from pypdf import PdfReader

from app.db import get_conn
from app.embeddings import embed_pasajes


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


def trocear(texto: str, tamaño: int = 800, solape: int = 100) -> list[str]:
    """Divide el texto en trozos de como máximo `tamaño` caracteres,
    con unos `solape` caracteres compartidos entre trozos consecutivos.
    No corta palabras."""
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

        trozo = texto[inicio:fin].strip()
        if trozo:
            trozos.append(trozo)
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


# ---------- Carga en base de datos ----------

def ingestar_pdf(conn, ruta: Path) -> int:
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

    registros = []
    for pagina, texto in leer_pdf(ruta):
        for trozo in trocear(texto):
            registros.append((pagina, trozo))

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