from pgvector.psycopg import register_vector

from app.db import get_conn
from app.embeddings import embed_pregunta
from app.schemas import Fuente

SQL_BUSCAR = """
    SELECT d.nombre,
           f.pagina,
           f.texto,
           1 - (f.embedding <=> %(v)s) AS similitud
    FROM fragmentos f
    JOIN documentos d ON d.id = f.documento_id
    ORDER BY f.embedding <=> %(v)s
    LIMIT %(k)s
"""


def buscar(pregunta: str, k: int = 5) -> list[Fuente]:
    """Devuelve los k fragmentos más parecidos a la pregunta."""
    vector = embed_pregunta(pregunta)
    with get_conn() as conn:
        register_vector(conn)
        filas = conn.execute(SQL_BUSCAR, {"v": vector, "k": k}).fetchall()
    return [
        Fuente(documento=n, pagina=p, texto=t, similitud=round(s, 4))
        for n, p, t, s in filas
    ]
