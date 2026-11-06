
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

## Evaluación 2026-11-04 14:45

Configuración: proveedor `groq`, k = 5, trozos de 800 caracteres, umbral 0.8

| Tipo | Preguntas | Recuperación @1 | Recuperación @5 | Respuesta correcta |
| --- | --- | --- | --- | --- |
| normal | 30 | 80 % | 100 % | 83 % |
| coloquial | 5 | 20 % | 60 % | 0 % |
| sin_respuesta | 5 | - | - | 100 % |
| TOTAL | 40 | 71 % | 94 % | 75 % |

Tiempo medio por pregunta: 7.9 s · Preguntas cortadas por el umbral (sin llamar a la IA): 1

Fallos:
- 03 [normal] ¿Cuántos días a la semana puedo teletrabajar si mi contrato es a jornada completa? → recuperó ['03_política_de_teletrabajo_para_personal_de_oficinas_centrales.pdf']
- 09 [normal] ¿Qué porcentaje de mi sueldo me corresponde si me bajo del trabajo por enfermedad y la baja supera los tres días? → recuperó ['09_bajas_por_enfermedad.pdf']
- 11 [normal] ¿Cuánto cuesta el kit de protección y en cuánto tiempo me lo reembolsan? → recuperó ['11_prevención_de_riesgos_laborales_en_pisos_y_cocina.pdf']
- 15 [normal] ¿Cuál es el salario mensual que me corresponde si me contrato para la temporada alta con jornada completa? → recuperó ['15_contratos_fijos_discontinuos_y_llamamiento_de_temporada.pdf']
- 18 [normal] ¿Cuál es el último día que puedo pedir la revisión de mi evaluación? → recuperó ['08_plus_de_nocturnidad_y_festivos.pdf']
- 31 [coloquial] Me he puesto malo, ¿qué tengo que hacer? → recuperó ['23_protocolo_contra_el_acoso_laboral_y_sexual.pdf']
- 32 [coloquial] Me quiero pirar de la empresa, ¿con cuánto tiempo aviso? → recuperó ['19_promoción_interna_y_vacantes.pdf']
- 33 [coloquial] ¿Me pagan algo más si curro un domingo? → recuperó ['08_plus_de_nocturnidad_y_festivos.pdf']
- 34 [coloquial] Me caso el mes que viene, ¿me dan días? → recuperó ['19_promoción_interna_y_vacantes.pdf']
- 35 [coloquial] Un compañero me está haciendo la vida imposible, ¿a quién se lo digo? → recuperó ['09_bajas_por_enfermedad.pdf']

## Evaluación 2026-11-04 15:03

Configuración: `groq` / `openai/gpt-oss-20b`, k = 5, trozos de 800 caracteres, umbral 0.8

| Tipo | Preguntas | Recuperación @1 | Recuperación @5 | Respuesta correcta |
| --- | --- | --- | --- | --- |
| normal | 30 | 80 % | 100 % | 87 % |
| coloquial | 5 | 20 % | 60 % | 20 % |
| sin_respuesta | 5 | - | - | 100 % |
| TOTAL | 40 | 71 % | 94 % | 80 % |

Tiempo medio por pregunta: 7.0 s · Preguntas cortadas por el umbral: 1

Fallos:
- 03 [normal] ¿Cuántos días a la semana puedo teletrabajar si mi contrato es a jornada completa? → recuperó ['03_política_de_teletrabajo_para_personal_de_oficinas_centrales.pdf']
- 11 [normal] ¿Cuánto cuesta el kit de protección y en cuánto tiempo me lo reembolsan? → recuperó ['11_prevención_de_riesgos_laborales_en_pisos_y_cocina.pdf']
- 15 [normal] ¿Cuál es el salario mensual que me corresponde si me contrato para la temporada alta con jornada completa? → recuperó ['15_contratos_fijos_discontinuos_y_llamamiento_de_temporada.pdf']
- 18 [normal] ¿Cuál es el último día que puedo pedir la revisión de mi evaluación? → recuperó ['08_plus_de_nocturnidad_y_festivos.pdf']
- 31 [coloquial] Me he puesto malo, ¿qué tengo que hacer? → recuperó ['23_protocolo_contra_el_acoso_laboral_y_sexual.pdf']
- 33 [coloquial] ¿Me pagan algo más si curro un domingo? → recuperó ['08_plus_de_nocturnidad_y_festivos.pdf']
- 34 [coloquial] Me caso el mes que viene, ¿me dan días? → recuperó ['19_promoción_interna_y_vacantes.pdf']
- 35 [coloquial] Un compañero me está haciendo la vida imposible, ¿a quién se lo digo? → recuperó ['09_bajas_por_enfermedad.pdf']

## Evaluación 2026-11-05 11:00

Configuración: `groq` / `openai/gpt-oss-20b`, k = 5, trozos de 800 caracteres, umbral 0.8, reformular True

| Tipo | Preguntas | Recuperación @1 | Recuperación @5 | Respuesta correcta |
| --- | --- | --- | --- | --- |
| normal | 30 | 73 % | 93 % | 80 % |
| coloquial | 5 | 60 % | 80 % | 40 % |
| sin_respuesta | 5 | - | - | 100 % |
| TOTAL | 40 | 71 % | 91 % | 78 % |

Tiempo medio por pregunta: 7.8 s · Preguntas cortadas por el umbral: 1

Fallos:
- 09 [normal] ¿Qué porcentaje de mi sueldo me corresponde si me bajo del trabajo por enfermedad y la baja supera los tres días? → recuperó ['09_bajas_por_enfermedad.pdf'] (consulta: «sueldo: porcentaje de salario correspondiente en baja por enfermedad superior a tres días de trabajo»)
- 11 [normal] ¿Cuánto cuesta el kit de protección y en cuánto tiempo me lo reembolsan? → recuperó ['26_gastos_de_viaje_y_dietas.pdf'] (consulta: «beneficios: costo del kit de protección y plazo de reembolso»)
- 15 [normal] ¿Cuál es el salario mensual que me corresponde si me contrato para la temporada alta con jornada completa? → recuperó ['15_contratos_fijos_discontinuos_y_llamamiento_de_temporada.pdf'] (consulta: «salario: remuneración mensual por contratación en temporada alta con jornada completa»)
- 18 [normal] ¿Cuál es el último día que puedo pedir la revisión de mi evaluación? → recuperó ['21_beneficios_sociales.pdf'] (consulta: «revisión de evaluación: plazo máximo para solicitud de revisión de desempeño laboral»)
- 23 [normal] ¿En qué horario puedo llamar al número confidencial de denuncias? → recuperó ['19_promoción_interna_y_vacantes.pdf'] (consulta: «horario de acceso al número confidencial de denuncias (línea de denuncias internas)»)
- 28 [normal] ¿Tengo que contestar algún mensaje de trabajo fuera del horario, y cuánto tiempo tengo para hacerlo? → recuperó ['21_beneficios_sociales.pdf'] (consulta: «responsabilidad de respuesta fuera de horario: plazos y requisitos para atender correos/emails laborales fuera de jornada»)
- 31 [coloquial] Me he puesto malo, ¿qué tengo que hacer? → recuperó ['09_bajas_por_enfermedad.pdf'] (consulta: «incapacidad laboral: procedimiento de notificación y documentación requerida»)
- 33 [coloquial] ¿Me pagan algo más si curro un domingo? → recuperó ['06_horas_extra_y_su_compensación.pdf'] (consulta: «horas extra: remuneración adicional por trabajo en día domingo»)
- 35 [coloquial] Un compañero me está haciendo la vida imposible, ¿a quién se lo digo? → recuperó ['29_código_ético_y_conflictos_de_interés.pdf'] (consulta: «procedimiento: reporte de conflicto laboral con compañero de trabajo, canal de comunicación interna y protocolo de mediación.»)

## Evaluación 2026-11-05 11:18

Configuración: `groq` / `openai/gpt-oss-20b`, k = 5, trozos de 800 caracteres, umbral 0.8, reformular True

| Tipo | Preguntas | Recuperación @1 | Recuperación @5 | Respuesta correcta |
| --- | --- | --- | --- | --- |
| normal | 30 | 87 % | 93 % | 67 % |
| coloquial | 5 | 40 % | 80 % | 20 % |
| sin_respuesta | 5 | - | - | 100 % |
| TOTAL | 40 | 80 % | 91 % | 65 % |

Tiempo medio por pregunta: 9.4 s · Preguntas cortadas por el umbral: 1

Fallos:
- 03 [normal] ¿Cuántos días a la semana puedo teletrabajar si mi contrato es a jornada completa? → recuperó ['03_política_de_teletrabajo_para_personal_de_oficinas_centrales.pdf'] (consulta: «teletrabajo: número de días a la semana permitidos bajo contrato a jornada completa<|endoftext|>Ok..??.. ...?.........»)
- 07 [normal] ¿Cuánto me pueden adelantar si necesito un anticipo? → recuperó ['07_nóminas.pdf'] (consulta: «anticipo salarial: condiciones, límites y procedimientos de solicitud y aprobación en la empresa.»)
- 09 [normal] ¿Qué porcentaje de mi sueldo me corresponde si me bajo del trabajo por enfermedad y la baja supera los tres días? → recuperó ['09_bajas_por_enfermedad.pdf'] (consulta: «remuneración: porcentaje a percibir en caso de baja médica superior a tres días de duración»)
- 15 [normal] ¿Cuál es el salario mensual que me corresponde si me contrato para la temporada alta con jornada completa? → recuperó ['15_contratos_fijos_discontinuos_y_llamamiento_de_temporada.pdf'] (consulta: «nómina: salario mensual por contratación a jornada completa durante la temporada alta»)
- 18 [normal] ¿Cuál es el último día que puedo pedir la revisión de mi evaluación? → recuperó ['25_protección_de_datos_de_clientes.pdf'] (consulta: «revisión de evaluación: fecha límite para solicitarla»)
- 20 [normal] ¿En qué fecha del mes me depositan la propina que me corresponde? → recuperó ['30_baja_voluntaria.pdf'] (consulta: «nómina: fecha de pago de la propina mensual»)
- 23 [normal] ¿En qué horario puedo llamar al número confidencial de denuncias? → recuperó ['23_protocolo_contra_el_acoso_laboral_y_sexual.pdf'] (consulta: «horario de atención del número confidencial de denuncias»)
- 24 [normal] Si me lleva a segunda falta en un año, ¿cuál sería la sanción económica? → recuperó ['07_nóminas.pdf'] (consulta: «sanción económica por segunda falta anual: política disciplinaria de la empresa»)
- 26 [normal] ¿Cuál es el tope diario para el alquiler de coche cuando viajo por trabajo? → recuperó ['26_gastos_de_viaje_y_dietas.pdf'] (consulta: «reembolso: límite diario de gasto por alquiler de vehículo en viajes laborales»)
- 27 [normal] ¿Con cuánto tiempo de antelación tengo que avisar si quiero solicitar una reducción de jornada? → recuperó ['30_baja_voluntaria.pdf'] (consulta: «reducir jornada: plazo de preaviso requerido para la solicitud de reducción de horario laboral»)
- 31 [coloquial] Me he puesto malo, ¿qué tengo que hacer? → recuperó ['09_bajas_por_enfermedad.pdf'] (consulta: «enfermedad: procedimiento de notificación de ausencia laboral por motivos de salud»)
- 33 [coloquial] ¿Me pagan algo más si curro un domingo? → recuperó ['06_horas_extra_y_su_compensación.pdf'] (consulta: «beneficios por trabajo dominical: compensación adicional y pago de horas extraordinarias en fin de semana»)
- 34 [coloquial] Me caso el mes que viene, ¿me dan días? → recuperó ['21_beneficios_sociales.pdf'] (consulta: «vacaciones matrimoniales: solicitud de días de licencia por matrimonio»)
- 35 [coloquial] Un compañero me está haciendo la vida imposible, ¿a quién se lo digo? → recuperó ['10_accidentes_laborales.pdf'] (consulta: «situación de conflicto laboral: protocolo de queja ante la dirección y recursos humanos»)

## Evaluación 2026-11-05 11:54

Configuración: `groq` / `openai/gpt-oss-120b`, k = 5, trozos de 800 caracteres, umbral 0.8, reformular True

| Tipo | Preguntas | Recuperación @1 | Recuperación @5 | Respuesta correcta |
| --- | --- | --- | --- | --- |
| normal | 30 | 93 % | 100 % | 87 % |
| coloquial | 5 | 60 % | 80 % | 40 % |
| sin_respuesta | 5 | - | - | 100 % |
| TOTAL | 40 | 89 % | 97 % | 82 % |

Tiempo medio por pregunta: 9.3 s · Preguntas cortadas por el umbral: 1

Fallos:
- 09 [normal] ¿Qué porcentaje de mi sueldo me corresponde si me bajo del trabajo por enfermedad y la baja supera los tres días? → recuperó ['09_bajas_por_enfermedad.pdf'] (consulta: «incapacidad temporal: porcentaje de salario durante baja por enfermedad superior a tres días»)
- 15 [normal] ¿Cuál es el salario mensual que me corresponde si me contrato para la temporada alta con jornada completa? → recuperó ['15_contratos_fijos_discontinuos_y_llamamiento_de_temporada.pdf'] (consulta: «remuneración: salario mensual para contrato de temporada alta a jornada completa»)
- 18 [normal] ¿Cuál es el último día que puedo pedir la revisión de mi evaluación? → recuperó ['18_evaluación_del_desempeño_anual.pdf'] (consulta: «evaluación de desempeño: fecha límite para solicitar revisión»)
- 20 [normal] ¿En qué fecha del mes me depositan la propina que me corresponde? → recuperó ['20_política_de_propinas.pdf'] (consulta: «propinas: fecha de depósito mensual»)
- 31 [coloquial] Me he puesto malo, ¿qué tengo que hacer? → recuperó ['23_protocolo_contra_el_acoso_laboral_y_sexual.pdf'] (consulta: «Me he puesto malo, ¿qué tengo que hacer?»)
- 33 [coloquial] ¿Me pagan algo más si curro un domingo? → recuperó ['06_horas_extra_y_su_compensación.pdf'] (consulta: «remuneración: compensación por trabajo en domingo»)
- 35 [coloquial] Un compañero me está haciendo la vida imposible, ¿a quién se lo digo? → recuperó ['23_protocolo_contra_el_acoso_laboral_y_sexual.pdf'] (consulta: «conflicto interpersonal: procedimiento de denuncia de conductas inapropiadas»)

## Evaluación 2026-11-05 12:24

Configuración: `groq` / `openai/gpt-oss-120b`, k = 5, trozos de 800 caracteres, umbral 0.8, reformular True

| Tipo | Preguntas | Recuperación @1 | Recuperación @5 | Respuesta correcta |
| --- | --- | --- | --- | --- |
| normal | 30 | 93 % | 100 % | 90 % |
| coloquial | 5 | 40 % | 80 % | 40 % |
| sin_respuesta | 5 | - | - | 100 % |
| TOTAL | 40 | 86 % | 97 % | 85 % |

Tiempo medio por pregunta: 9.4 s · Preguntas cortadas por el umbral: 1

Fallos:
- 09 [normal] ¿Qué porcentaje de mi sueldo me corresponde si me bajo del trabajo por enfermedad y la baja supera los tres días? → recuperó ['09_bajas_por_enfermedad.pdf'] (consulta: «incapacidad temporal: porcentaje de salario durante baja por enfermedad superior a tres días»)
- 18 [normal] ¿Cuál es el último día que puedo pedir la revisión de mi evaluación? → recuperó ['18_evaluación_del_desempeño_anual.pdf'] (consulta: «evaluación de desempeño: fecha límite para solicitar revisión»)
- 20 [normal] ¿En qué fecha del mes me depositan la propina que me corresponde? → recuperó ['20_política_de_propinas.pdf'] (consulta: «propinas: fecha de depósito mensual»)
- 31 [coloquial] Me he puesto malo, ¿qué tengo que hacer? → recuperó ['23_protocolo_contra_el_acoso_laboral_y_sexual.pdf'] (consulta: «Me he puesto malo, ¿qué tengo que hacer?»)
- 33 [coloquial] ¿Me pagan algo más si curro un domingo? → recuperó ['06_horas_extra_y_su_compensación.pdf'] (consulta: «remuneración: compensación por trabajo en domingo»)
- 35 [coloquial] Un compañero me está haciendo la vida imposible, ¿a quién se lo digo? → recuperó ['29_código_ético_y_conflictos_de_interés.pdf'] (consulta: «conflicto interpersonal: procedimiento para reportar conductas problemáticas de compañeros»)

## Evaluación 2026-11-05 17:20

Configuración: `groq` / `openai/gpt-oss-120b`, k = 5, trozos de 500 caracteres, umbral 0.8, reformular True

| Tipo | Preguntas | Recuperación @1 | Recuperación @5 | Respuesta correcta |
| --- | --- | --- | --- | --- |
| normal | 30 | 90 % | 100 % | 87 % |
| coloquial | 5 | 60 % | 80 % | 60 % |
| sin_respuesta | 5 | - | - | 100 % |
| TOTAL | 40 | 86 % | 97 % | 85 % |

Tiempo medio por pregunta: 5.4 s · Preguntas cortadas por el umbral: 1

Fallos:
- 09 [normal] ¿Qué porcentaje de mi sueldo me corresponde si me bajo del trabajo por enfermedad y la baja supera los tres días? → recuperó ['09_bajas_por_enfermedad.pdf'] (consulta: «incapacidad temporal: porcentaje de salario durante baja por enfermedad superior a tres días»)
- 13 [normal] ¿Cuánto me sale el menú del comedor si uso la credencial? → recuperó ['13_comidas_del_personal_y_comedor_de_empleados.pdf'] (consulta: «¿Cuánto me sale el menú del comedor si uso la credencial?»)
- 20 [normal] ¿En qué fecha del mes me depositan la propina que me corresponde? → recuperó ['20_política_de_propinas.pdf'] (consulta: «propinas: fecha de depósito mensual»)
- 29 [normal] ¿En cuánto tiempo debo comunicar un posible conflicto de interés una vez que lo descubro? → recuperó ['29_código_ético_y_conflictos_de_interés.pdf'] (consulta: «conflicto de interés: plazo para comunicar su descubrimiento»)
- 31 [coloquial] Me he puesto malo, ¿qué tengo que hacer? → recuperó ['23_protocolo_contra_el_acoso_laboral_y_sexual.pdf'] (consulta: «Me he puesto malo, ¿qué tengo que hacer?»)
- 33 [coloquial] ¿Me pagan algo más si curro un domingo? → recuperó ['06_horas_extra_y_su_compensación.pdf'] (consulta: «remuneración: compensación por trabajo en domingo»)

## Evaluación 2026-11-06 10:01

Configuración: `groq` / `openai/gpt-oss-120b`, k = 5, trozos de 500 caracteres, umbral 0.8, reformular True

| Tipo | Preguntas | Recuperación @1 | Recuperación @5 | Respuesta correcta |
| --- | --- | --- | --- | --- |
| normal | 30 | 83 % | 97 % | 90 % |
| coloquial | 5 | 80 % | 100 % | 40 % |
| sin_respuesta | 5 | - | - | 100 % |
| TOTAL | 40 | 83 % | 97 % | 85 % |

Tiempo medio por pregunta: 4.8 s · Preguntas cortadas por el umbral: 1

Fallos:
- 13 [normal] ¿Cuánto me sale el menú del comedor si uso la credencial? → recuperó ['13_comidas_del_personal_y_comedor_de_empleados.pdf'] (consulta: «beneficio de comedor: precio del menú con credencial»)
- 20 [normal] ¿En qué fecha del mes me depositan la propina que me corresponde? → recuperó ['30_baja_voluntaria.pdf'] (consulta: «nómina: fecha de depósito de la gratificación (propina) mensual»)
- 29 [normal] ¿En cuánto tiempo debo comunicar un posible conflicto de interés una vez que lo descubro? → recuperó ['29_código_ético_y_conflictos_de_interés.pdf'] (consulta: «conflicto de interés: plazo para comunicar posible conflicto tras su detección»)
- 31 [coloquial] Me he puesto malo, ¿qué tengo que hacer? → recuperó ['09_bajas_por_enfermedad.pdf'] (consulta: «incapacidad temporal: procedimiento y notificación de enfermedad al empleador»)
- 33 [coloquial] ¿Me pagan algo más si curro un domingo? → recuperó ['06_horas_extra_y_su_compensación.pdf'] (consulta: «remuneración adicional: pago extra por trabajo en domingo»)
- 35 [coloquial] Un compañero me está haciendo la vida imposible, ¿a quién se lo digo? → recuperó ['23_protocolo_contra_el_acoso_laboral_y_sexual.pdf'] (consulta: «conflicto interpersonal: reporte de acoso o conducta problemá»)
