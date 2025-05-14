from pydantic import BaseModel

class Salida(BaseModel):
    estatus: str
    mensaje: str
