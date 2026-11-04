from app.embeddings import embed_pasajes, embed_pregunta

pregunta = "¿Cuántos días libres tengo al año?"
frases = [
    "Cada empleado disfruta de 30 días naturales de vacaciones anuales.",
    "El uniforme debe estar limpio y planchado al inicio del turno.",
    "Las nóminas se abonan el último día hábil de cada mes.",
]

q = embed_pregunta(pregunta)
p = embed_pasajes(frases)
similitudes = p @ q  # producto escalar = similitud coseno (vectores normalizados)

print(f"Pregunta: {pregunta}\n")
for frase, sim in sorted(zip(frases, similitudes), key=lambda x: -x[1]):
    print(f"{sim:.3f}  {frase}")
