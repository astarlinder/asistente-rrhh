
## Evaluación 2026-11-04 13:59

Configuración: proveedor `gemini`, k = 5, trozos de 800 caracteres, umbral 0.8

| Tipo | Preguntas | Recuperación @1 | Recuperación @5 | Respuesta correcta |
| --- | --- | --- | --- | --- |
| normal | 30 | 80 % | 100 % | 83 % |
| coloquial | 5 | 20 % | 60 % | 40 % |
| sin_respuesta | 5 | - | - | 100 % |
| TOTAL | 40 | 71 % | 94 % | 80 % |

Tiempo medio por pregunta: 7.9 s · Preguntas cortadas por el umbral (sin llamar a la IA): 1

Fallos:
- 09 [normal] ¿Qué porcentaje de mi sueldo me corresponde si me bajo del trabajo por enfermedad y la baja supera los tres días? → recuperó ['09_bajas_por_enfermedad.pdf']
- 11 [normal] ¿Cuánto cuesta el kit de protección y en cuánto tiempo me lo reembolsan? → recuperó ['11_prevención_de_riesgos_laborales_en_pisos_y_cocina.pdf']
- 15 [normal] ¿Cuál es el salario mensual que me corresponde si me contrato para la temporada alta con jornada completa? → recuperó ['15_contratos_fijos_discontinuos_y_llamamiento_de_temporada.pdf']
- 16 [normal] ¿Cuánto me van a pagar de bono si termino el periodo de prueba con una puntuación suficiente? → recuperó ['16_periodo_de_prueba_e_incorporación.pdf']
- 18 [normal] ¿Cuál es el último día que puedo pedir la revisión de mi evaluación? → recuperó ['08_plus_de_nocturnidad_y_festivos.pdf']
- 32 [coloquial] Me quiero pirar de la empresa, ¿con cuánto tiempo aviso? → recuperó ['19_promoción_interna_y_vacantes.pdf']
- 34 [coloquial] Me caso el mes que viene, ¿me dan días? → recuperó ['19_promoción_interna_y_vacantes.pdf']
- 35 [coloquial] Un compañero me está haciendo la vida imposible, ¿a quién se lo digo? → recuperó ['09_bajas_por_enfermedad.pdf']
