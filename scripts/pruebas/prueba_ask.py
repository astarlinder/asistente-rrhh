from app.rag import preguntar

preguntas = [
    "¿Cuántos días de vacaciones tengo al año?",
    "¿Cuánto me pagan por trabajar de noche?",
    "Me he puesto malo, ¿qué tengo que hacer?",
    "¿Quién ganó el último Mundial de fútbol?",
]

for p in preguntas:
    r = preguntar(p)
    print(f"\nPREGUNTA: {p}")
    print(f"[{r.proveedor}] {r.respuesta}")
