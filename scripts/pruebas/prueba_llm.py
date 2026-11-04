from app.llm import responder

r = responder(
    "¿Cuántos días de vacaciones tiene un trabajador en España según el Estatuto?",
    system="Responde en una sola frase, en español.",
)
print(f"[{r['proveedor']}] {r['texto']}")
