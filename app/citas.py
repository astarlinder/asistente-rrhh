import re
import unicodedata

CITA = re.compile(r"([\w\-.]+\.pdf),\s*pág\.\s*(\d+)", re.IGNORECASE)
ETIQUETA = re.compile(r"\bFuentes?\s*\d+", re.IGNORECASE)


def _norm(nombre: str) -> str:
    return unicodedata.normalize("NFC", nombre).lower()


def validar_citas(texto: str, fuentes: set[tuple[str, int]]) -> list[str]:
    """Devuelve las citas del texto que no corresponden a ninguna fuente recuperada.

    `fuentes` es el conjunto de (documento, página) que llegó al modelo.
    También marca las etiquetas del tipo «Fuente 1», que no son citas válidas.
    """
    permitidas = {(_norm(d), int(p)) for d, p in fuentes}
    invalidas = [
        m.group(0)
        for m in CITA.finditer(texto)
        if (_norm(m.group(1)), int(m.group(2))) not in permitidas
    ]
    invalidas += ETIQUETA.findall(texto)
    return invalidas
