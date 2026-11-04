"""Genera documentos ficticios de RR. HH. de Hoteles Tramuntana en PDF."""
from pathlib import Path

from fpdf import FPDF

from app.llm import responder

CARPETA = Path("data")
CARPETA.mkdir(exist_ok=True)
FUENTE = r"C:\Windows\Fonts\arial.ttf"

TEMAS = [
    "Política de vacaciones",
    "Permisos retribuidos (matrimonio, nacimiento, fallecimiento, mudanza)",
    "Política de teletrabajo para personal de oficinas centrales",
    "Horarios y turnos en hotel (recepción, pisos, cocina, sala)",
    "Registro de jornada y fichajes",
    "Horas extra y su compensación",
    "Nóminas: fechas de pago, conceptos y anticipos",
    "Plus de nocturnidad y festivos",
    "Bajas por enfermedad: comunicación y justificantes",
    "Accidentes laborales: protocolo de actuación",
    "Prevención de riesgos laborales en pisos y cocina",
    "Uniformes y normas de imagen personal",
    "Comidas del personal y comedor de empleados",
    "Alojamiento para personal de temporada",
    "Contratos fijos discontinuos y llamamiento de temporada",
    "Periodo de prueba e incorporación (onboarding)",
    "Formación interna e idiomas",
    "Evaluación del desempeño anual",
    "Promoción interna y vacantes",
    "Política de propinas",
    "Beneficios sociales: descuentos en hoteles del grupo",
    "Seguro médico y retribución flexible",
    "Protocolo contra el acoso laboral y sexual",
    "Uso del móvil y redes sociales durante el trabajo",
    "Protección de datos de clientes (RGPD) para el personal",
    "Gastos de viaje y dietas",
    "Excedencias y reducción de jornada",
    "Desconexión digital",
    "Código ético y conflictos de interés",
    "Baja voluntaria: preaviso y finiquito",
]

SYSTEM = (
    "Eres el departamento de RR. HH. de Hoteles Tramuntana, una cadena ficticia de "
    "8 hoteles en Mallorca con unos 900 empleados. Redactas políticas internas en "
    "español, claras y concretas. Incluye siempre cifras específicas (días, euros, "
    "plazos, horarios, porcentajes), quién es responsable y cómo se solicita. "
    "Usa texto plano: títulos en MAYÚSCULAS y apartados numerados, sin markdown, "
    "sin asteriscos ni almohadillas. Entre 600 y 900 palabras."
)


def guardar_pdf(titulo: str, texto: str, ruta: Path) -> None:
    pdf = FPDF()
    pdf.add_font("Arial", "", FUENTE)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.multi_cell(0, 8, f"HOTELES TRAMUNTANA - {titulo.upper()}")
    pdf.ln(4)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 5, texto)
    pdf.output(str(ruta))


for n, tema in enumerate(TEMAS, start=1):
    ruta = CARPETA / f"{n:02d}_{tema.split(' (')[0].split(':')[0].lower().replace(' ', '_')}.pdf"
    if ruta.exists():
        print(f"Ya existe, salto: {ruta.name}")
        continue
    r = responder(f"Redacta la política interna: {tema}.", system=SYSTEM)
    guardar_pdf(tema, r["texto"], ruta)
    print(f"[{r['proveedor']}] {ruta.name}")