from pydantic import BaseModel
from typing import Optional


#Clase para definir el servicio Gestión de usuarios con la operación de consultar Usario por ID
class UsuarioSalida(BaseModel):
    idUsuario: str
    nombre: str
    email: str
    telefono: str
    tipo: str  # Cliente, Barbero, Admin
    estatus: str
