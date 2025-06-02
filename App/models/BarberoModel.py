from pydantic import BaseModel
from typing import List, Optional

class BarberoUsuario(BaseModel):
    nombre: str
    correo: str
    telefono: str
    tipo: str

class BarberoBarberia(BaseModel):
    nombre: str
    direccion: str

class BarberoVista(BaseModel):
    idBarbero: int
    especialidad: str
    horario: str
    usuario: BarberoUsuario
    barberia: BarberoBarberia

class BarberosVistaSalida(BaseModel):
    estatus: str
    mensaje: str
    barberos: Optional[List[BarberoVista]] = []

class BarberoSalida(BaseModel):
    estatus: str
    mensaje: str
    barbero: Optional[BarberoVista] = None
