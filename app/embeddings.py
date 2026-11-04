from functools import lru_cache

import numpy as np
from sentence_transformers import SentenceTransformer

MODELO = "intfloat/multilingual-e5-small"
DIMENSIONES = 384


@lru_cache
def _modelo() -> SentenceTransformer:
    """Carga el modelo una sola vez y lo reutiliza."""
    return SentenceTransformer(MODELO)


def embed_pasajes(textos: list[str]) -> np.ndarray:
    """Embeddings de los trozos de documento."""
    return _modelo().encode(
        [f"passage: {t}" for t in textos],
        normalize_embeddings=True,
        batch_size=32,
        show_progress_bar=len(textos) > 50,
    )


def embed_pregunta(texto: str) -> np.ndarray:
    """Embedding de una pregunta del usuario."""
    return _modelo().encode(f"query: {texto}", normalize_embeddings=True)