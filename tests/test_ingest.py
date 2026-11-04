import pytest

from app.ingest import limpiar, trocear


def test_limpiar_quita_espacios_y_saltos():
    assert limpiar("Hola   mundo\n\n  adiós ") == "Hola mundo adiós"


def test_texto_corto_da_un_solo_trozo():
    assert trocear("Texto corto", tamaño=800, solape=100) == ["Texto corto"]


def test_texto_vacio_no_da_trozos():
    assert trocear("   ", tamaño=800, solape=100) == []


def test_ningun_trozo_supera_el_tamaño():
    texto = "palabra " * 1000
    trozos = trocear(texto, tamaño=200, solape=50)
    assert len(trozos) > 1
    assert all(len(t) <= 200 for t in trozos)


def test_trozos_consecutivos_comparten_texto():
    texto = " ".join(f"p{i}" for i in range(500))
    trozos = trocear(texto, tamaño=200, solape=50)
    final_del_primero = trozos[0][-20:]
    assert final_del_primero in trozos[1]


def test_no_corta_palabras():
    texto = " ".join(["vacaciones"] * 300)
    for trozo in trocear(texto, tamaño=200, solape=50):
        for palabra in trozo.split(" "):
            assert palabra == "vacaciones"


def test_solape_mayor_que_tamaño_da_error():
    with pytest.raises(ValueError):
        trocear("texto", tamaño=100, solape=100)
