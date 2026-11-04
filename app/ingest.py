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