from app import rag
from app.schemas import Fuente


def fuente(similitud: float) -> Fuente:
    return Fuente(
        documento="01_vacaciones.pdf", pagina=1, texto="30 días", similitud=similitud
    )


def test_similitud_baja_no_llama_a_la_ia(monkeypatch):
    monkeypatch.setattr(rag, "buscar", lambda p, k: [fuente(0.70)])

    def no_deberia_llamarse(*args, **kwargs):
        raise AssertionError("Se ha llamado a la IA con similitud baja")

    monkeypatch.setattr(rag, "responder", no_deberia_llamarse)

    r = rag.preguntar("¿Quién ganó el Mundial?")
    assert r.respuesta == rag.NO_APARECE
    assert r.proveedor == "ninguno"
    assert r.fuentes == []


def test_similitud_alta_llama_a_la_ia(monkeypatch):
    monkeypatch.setattr(rag, "buscar", lambda p, k: [fuente(0.87)])
    monkeypatch.setattr(
        rag,
        "responder",
        lambda prompt, system: {"texto": "Tienes 30 días.", "proveedor": "falso"},
    )

    r = rag.preguntar("¿Cuántos días de vacaciones tengo?")
    assert r.respuesta == "Tienes 30 días."
    assert r.proveedor == "falso"
    assert len(r.fuentes) == 1


def test_sin_fuentes_no_llama_a_la_ia(monkeypatch):
    monkeypatch.setattr(rag, "buscar", lambda p, k: [])
    r = rag.preguntar("lo que sea")
    assert r.respuesta == rag.NO_APARECE
