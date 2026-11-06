import os

import httpx
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")

EJEMPLOS = [
    "¿Cuántos días de vacaciones tengo al año?",
    "¿Cuánto me pagan por trabajar de noche?",
    "¿Puedo trabajar desde casa?",
    "¿Cuánto dura el periodo de prueba?",
]


def usar_ejemplo(texto: str) -> None:
    st.session_state.pregunta = texto


st.set_page_config(page_title="Asistente RR. HH.", page_icon="🏨")
st.title("Asistente de RR. HH.")
st.caption("Hoteles Tramuntana · Respuestas basadas en la documentación interna")

with st.sidebar:
    st.subheader("Preguntas de ejemplo")
    for e in EJEMPLOS:
        st.button(e, on_click=usar_ejemplo, args=(e,), use_container_width=True)

pregunta = st.text_input("Escribe tu pregunta", key="pregunta")

if st.button("Preguntar", type="primary") and pregunta:
    with st.spinner("Buscando en la documentación..."):
        try:
            r = httpx.post(f"{API_URL}/ask", json={"texto": pregunta}, timeout=60)
            r.raise_for_status()
            datos = r.json()
        except httpx.HTTPError as e:
            st.error(f"No se pudo conectar con la API: {e}")
            st.stop()

    st.markdown(datos["respuesta"])
    st.caption(f"Respondido por: {datos['proveedor']}")

    if datos["fuentes"]:
        with st.expander(f"Ver las {len(datos['fuentes'])} fuentes consultadas"):
            for f in datos["fuentes"]:
                st.markdown(
                    f"**{f['documento']}**, pág. {f['pagina']} · "
                    f"similitud {f['similitud']:.3f}"
                )
                st.text(f["texto"][:500] + "...")
