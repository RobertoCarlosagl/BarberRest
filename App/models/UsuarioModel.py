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

class LoginEntrada(BaseModel):
    correo: str
    password: str

class UsuarioAutenticado(BaseModel):
    idUsuario: str
    nombre: str
    correo: str
    tipo: str
    estatus: str

class LoginRespuesta(BaseModel):
    estatus: str
    mensaje: str
    usuario: Optional[UsuarioAutenticado] = None