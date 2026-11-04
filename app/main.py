from fastapi import FastAPI

from app.config import settings
from app.db import get_conn

app = FastAPI(title="Asistente RR. HH.", version="0.1.0")


@app.get("/health")
def health() -> dict:
    with get_conn() as conn:
        n_fragmentos = conn.execute("SELECT count(*) FROM fragmentos").fetchone()[0]
    return {
        "ok": True,
        "llm_provider": settings.llm_provider,
        "fragmentos": n_fragmentos,
    }