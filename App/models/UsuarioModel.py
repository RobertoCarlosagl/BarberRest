from pydantic import BaseModel
from typing import Optional


#Clase para definir el servicio Gestión de usuarios con la operación de consultar Usario por ID
class UsuarioSalida(BaseModel):
    idUsuario: str
    nombre: str
    apellido: str
    correo: str
    telefono: str
    tipo: str
    estatus: str
