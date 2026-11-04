import re
from pathlib import Path

from pypdf import PdfReader


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