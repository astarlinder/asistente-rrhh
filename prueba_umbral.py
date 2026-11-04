from app.search import buscar

relevantes = [
    "¿Cuántos días de vacaciones tengo al año?",
    "¿Cuándo me pagan la nómina?",
    "¿Puedo trabajar desde casa?",
    "¿Cuánto me pagan por trabajar de noche?",
    "¿Qué pasa si me quiero ir de la empresa?",
    "¿Me dan uniforme?",
    "¿Hay comedor para empleados?",
    "¿Cuánto dura el periodo de prueba?",
]

irrelevantes = [
    "¿Quién ganó el último Mundial de fútbol?",
    "¿Cuál es la capital de Australia?",
    "Dame una receta de paella",
    "¿Qué tiempo hará mañana en Palma?",
    "¿Cómo se instala Python?",
    "¿Cuántos habitantes tiene Mallorca?",
]

print("RELEVANTES")
for p in relevantes:
    print(f"  {buscar(p, k=1)[0].similitud:.3f}  {p}")

print("\nIRRELEVANTES")
for p in irrelevantes:
    print(f"  {buscar(p, k=1)[0].similitud:.3f}  {p}")