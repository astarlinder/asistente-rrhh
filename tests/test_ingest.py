import pytest

from app.ingest import limpiar, trocear, trocear_paginas


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


def test_trocear_paginas_no_corta_frase_entre_paginas():
    paginas = [
        (1, "Texto inicial. La distribución se efectuará mediante transferencia a la"),
        (2, "cuenta del empleado el día 15 del mes. Otro texto."),
    ]
    trozos = trocear_paginas(paginas, tamaño=300, solape=20)
    frase = "transferencia a la cuenta del empleado el día 15"
    assert any(frase in t for _, t in trozos)


def test_trocear_paginas_asigna_pagina_de_inicio():
    paginas = [(1, "uno " * 100), (2, "dos " * 100)]
    trozos = trocear_paginas(paginas, tamaño=150, solape=20)
    assert trozos[0][0] == 1
    assert trozos[-1][0] == 2
    assert [p for p, _ in trozos] == sorted(p for p, _ in trozos)
