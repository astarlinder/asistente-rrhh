from app.search import buscar

preguntas = [
    "¿Cuántos días de vacaciones tengo al año?",
    "¿Cuándo me pagan la nómina?",
    "Me he puesto malo, ¿qué tengo que hacer?",
    "¿Puedo trabajar desde casa?",
    "¿Cuánto me pagan por trabajar de noche?",
    "¿Qué pasa si me quiero ir de la empresa?",
]

for p in preguntas:
    print(f"\n{p}")
    for f in buscar(p, k=3):
        print(f"   {f.similitud:.3f}  {f.documento} (pág. {f.pagina})")