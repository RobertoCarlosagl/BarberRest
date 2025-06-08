from pydantic import BaseModel, Field, EmailStr
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

    # ✅ Modelo usado cuando un nuevo usuario se registra desde el frontend o Swagger


class UsuarioRegistro(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=30, description="Nombre del usuario")
    apellido: str = Field(..., min_length=2, max_length=30, description="Apellido del usuario")
    correo: EmailStr = Field(..., description="Correo electrónico único del usuario")
    telefono: str = Field(..., min_length=10, max_length=15, description="Teléfono de contacto")
    password: str = Field(..., min_length=4, max_length=20, description="Contraseña del usuario")

    # ✅ Modelo usado solo por el Admin para cambiar el rol de un usuario existente


class CambioRol(BaseModel):
    nuevo_rol: str = Field(..., pattern="^(Admin|Barbero)$", description="Nuevo rol: Admin o Barbero")


