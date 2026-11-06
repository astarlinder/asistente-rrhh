import os

from app.rag import preguntar

PREGUNTAS = [
    "¿Cuánto me pueden adelantar si necesito un anticipo?",
    "¿Qué porcentaje de mi sueldo me corresponde si me bajo del trabajo por enfermedad y la baja supera los tres días?",
    "¿Cuál es el salario mensual que me corresponde si me contrato para la temporada alta con jornada completa?",
    "¿En qué fecha del mes me depositan la propina que me corresponde?",
    "¿Con cuánto tiempo de antelación tengo que avisar si quiero solicitar una reducción de jornada?",
    "Me caso el mes que viene, ¿me dan días?",
]

print("Modelo Groq:", os.getenv("GROQ_MODEL", "(el de .env)"))
for p in PREGUNTAS:
    r = preguntar(p)
    print(f"\n{p}\n -> {r.respuesta}  [{r.proveedor}]")
