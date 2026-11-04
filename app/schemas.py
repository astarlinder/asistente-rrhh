from pydantic import BaseModel, Field


class Pregunta(BaseModel):
    texto: str = Field(..., min_length=3, examples=["¿Cuántos días de vacaciones tengo?"])
    k: int = Field(5, ge=1, le=20, description="Número de fragmentos a devolver")


class Fuente(BaseModel):
    documento: str
    pagina: int
    texto: str
    similitud: float


class Respuesta(BaseModel):
    respuesta: str
    proveedor: str
    fuentes: list[Fuente]