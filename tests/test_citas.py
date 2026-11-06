import unicodedata

from app.citas import validar_citas

FUENTES = {("07_nóminas.pdf", 1), ("30_baja_voluntaria.pdf", 1)}


def test_cita_valida():
    assert validar_citas("Hasta 500 € (07_nóminas.pdf, pág. 1).", FUENTES) == []


def test_documento_inventado():
    assert validar_citas("Son 5 días (99_inventado.pdf, pág. 1).", FUENTES) == [
        "99_inventado.pdf, pág. 1"
    ]


def test_pagina_no_recuperada():
    assert validar_citas("(07_nóminas.pdf, pág. 7)", FUENTES) == [
        "07_nóminas.pdf, pág. 7"
    ]


def test_etiqueta_fuente_es_invalida():
    assert validar_citas("Se paga al 200 % (Fuente 1, pág. 1).", FUENTES) == [
        "Fuente 1"
    ]


def test_sin_citas_no_da_error():
    assert validar_citas("No aparece en la documentación de RR. HH.", FUENTES) == []


def test_acentos_en_distinta_normalizacion():
    texto = unicodedata.normalize("NFD", "(07_nóminas.pdf, pág. 1)")
    assert validar_citas(texto, FUENTES) == []
