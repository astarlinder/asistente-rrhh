import re

from app.citas import validar_citas
from app.config import settings
from app.llm import responder
from app.schemas import Fuente, Respuesta
from app.search import buscar

NO_APARECE = "No aparece en la documentación de RR. HH."

SYSTEM = """Eres el asistente de RR. HH. de Hoteles Tramuntana. Respondes a empleados usando EXCLUSIVAMENTE las fuentes que se te dan.

Reglas:
1. Lee todas las fuentes antes de responder. Si varias tratan el tema, usa la que responde exactamente a lo que se pregunta y completa con las demás si aportan datos necesarios.
2. Si la respuesta depende de una condición (antigüedad, tipo de contrato, jornada...) que la pregunta no indica, da todos los casos que aparezcan, diciendo a qué condición corresponde cada uno. No presentes como regla general lo que es una excepción.
3. No equipares casos distintos (por ejemplo, vacaciones y permisos retribuidos). Si una fuente trata un caso parecido pero no el preguntado, dilo en vez de aplicarlo.
4. Si la información no aparece en las fuentes, responde exactamente: "No aparece en la documentación de RR. HH."
5. Cita cada dato así: (nombre_del_documento.pdf, pág. N), copiando el nombre de la cabecera de la fuente. Nunca escribas "Fuente 1" ni inventes documentos o páginas.
6. Responde en español, de forma breve y con las cifras exactas."""

# Ejemplos DISTINTOS a los del set de evaluación, para no hacer trampa
REFORMULAR = """Reescribe la pregunta de un empleado de hotel como una consulta de búsqueda
para la documentación interna de RR. HH., usando términos formales de recursos humanos
y sinónimos de las palabras clave (el término formal junto al coloquial).

Reescribe SIEMPRE, también si la pregunta ya parece clara. Solo si es claramente ajena
al trabajo y a RR. HH. (deportes, cocina, ocio...), devuélvela sin cambios.

Ejemplos:
- "¿cuándo cobro?" -> "nómina: fecha de pago del salario mensual"
- "¿puedo usar el móvil en el curro?" -> "uso del teléfono móvil durante la jornada laboral"
- "me han dado un golpe en la cocina" -> "accidente laboral: protocolo de actuación y comunicación"

Devuelve SOLO la consulta, en una línea, sin comillas ni explicaciones."""


def construir_contexto(fuentes: list[Fuente]) -> str:
    return "\n\n".join(
        f"[Fuente {i}] {f.documento}, pág. {f.pagina}\n{f.texto}"
        for i, f in enumerate(fuentes, start=1)
    )


def reformular(pregunta: str) -> str:
    texto = responder(pregunta, system=REFORMULAR)["texto"]
    return limpiar_consulta(texto, pregunta)


def combinar(a: list[Fuente], b: list[Fuente], k: int) -> list[Fuente]:
    """Junta dos listas de resultados, quita duplicados y deja los k mejores."""
    mejores: dict[tuple, Fuente] = {}
    for f in a + b:
        clave = (f.documento, f.pagina, f.texto[:80])
        if clave not in mejores or f.similitud > mejores[clave].similitud:
            mejores[clave] = f
    return sorted(mejores.values(), key=lambda f: -f.similitud)[:k]


def preguntar(pregunta: str, k: int = 5) -> Respuesta:
    fuentes = buscar(pregunta, k)

    # Primera barrera: si nada se parece, no llamamos a la IA (ni para reformular)
    if not fuentes or fuentes[0].similitud < settings.umbral_similitud:
        return Respuesta(respuesta=NO_APARECE, proveedor="ninguno", fuentes=[])

    # Búsqueda doble: pregunta original + pregunta reformulada
    consulta = None
    if settings.reformular:
        consulta = reformular(pregunta)
        if consulta.lower() != pregunta.lower():
            fuentes = combinar(fuentes, buscar(consulta, k), k)

        prompt = f"FUENTES:\n\n{construir_contexto(fuentes)}\n\nPREGUNTA: {pregunta}"
    r = responder(prompt, system=SYSTEM)
    recuperadas = {(f.documento, f.pagina) for f in fuentes}
    return Respuesta(
        respuesta=r["texto"],
        proveedor=r["proveedor"],
        fuentes=fuentes,
        consulta=consulta,
        citas_invalidas=validar_citas(r["texto"], recuperadas),
    )


def limpiar_consulta(texto: str, original: str) -> str:
    """Normaliza la consulta reformulada; si queda vacía, usa la pregunta original."""
    texto = re.sub(r"<\|[^|>]*\|>", " ", texto)  # tokens especiales tipo <|endoftext|>
    texto = " ".join(texto.split())  # une líneas y colapsa espacios
    texto = texto.strip(" \"'«»")
    return texto[:300] if texto else original
