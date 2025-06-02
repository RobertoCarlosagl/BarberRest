from pydantic import BaseModel
from typing import List, Optional

class Servicio(BaseModel):
    idServicio: int
    nombre: str
    precio: float
    especialidad: str
    caracteristicas: str

class ServiciosSalida(BaseModel):
    estatus: str
    mensaje: str
    servicios: Optional[List[Servicio]] = []

class ServicioSalida(BaseModel):
    estatus: str
    mensaje: str
    servicio: Optional[Servicio] = None
