from fastapi import FastAPI

from app.config import settings
from app.db import get_conn
from app.schemas import Fuente, Pregunta
from app.search import buscar
from app.rag import preguntar
from app.schemas import Fuente, Pregunta, Respuesta

app = FastAPI(title="Asistente RR. HH.", version="0.2.0")


@app.get("/health")
def health() -> dict:
    with get_conn() as conn:
        n_fragmentos = conn.execute("SELECT count(*) FROM fragmentos").fetchone()[0]
    return {
        "ok": True,
        "llm_provider": settings.llm_provider,
        "fragmentos": n_fragmentos,
    }


@app.post("/search", response_model=list[Fuente])
def search(pregunta: Pregunta) -> list[Fuente]:
    """Búsqueda semántica: devuelve los fragmentos más relevantes."""
    return buscar(pregunta.texto, pregunta.k)


@app.post("/ask", response_model=Respuesta)
def ask(pregunta: Pregunta) -> Respuesta:
    """Responde a la pregunta usando los documentos de RR. HH. con citas."""
    return preguntar(pregunta.texto, pregunta.k)