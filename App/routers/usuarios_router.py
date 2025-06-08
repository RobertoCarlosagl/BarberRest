from fastapi import APIRouter, Request
from App.models.UsuarioModel import (
    UsuarioSalida,         # Modelo de salida para consultar usuario
    LoginEntrada,          # Modelo de entrada para autenticación
    LoginRespuesta,        # Modelo de salida para autenticación
    UsuarioRegistro,       # Modelo para registrar nuevo usuario
    CambioRol              # Modelo para cambiar el rol de un usuario
)
from App.models.RespuestaModel import Salida
from App.dao.UsuarioDAO import UsuarioDAO
router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


#ruta para consultar usuario por su ID
@router.get("/{idUsuario}", response_model=UsuarioSalida | Salida)
def consultar_usuario_por_id(idUsuario: str, request: Request):
    dao = UsuarioDAO(request.app.db)
    return dao.consultarUsuarioPorId(idUsuario)
from App.models.UsuarioModel import LoginEntrada, LoginRespuesta

@router.post("/autenticar", response_model=LoginRespuesta, summary="Autenticación de usuarios")
def autenticar_usuario(login: LoginEntrada, request: Request):
    dao = UsuarioDAO(request.app.db)
    return dao.autenticarUsuario(login.correo, login.password)




# Definimos el router de usuarios
router = APIRouter(
    prefix="/usuarios",
    tags=["Gestión de Usuarios"]
)

# ✅ Ruta para consultar un usuario por su ID
@router.get("/{idUsuario}", response_model=UsuarioSalida | Salida, summary="Consultar Usuario por ID")
def consultar_usuario_por_id(idUsuario: str, request: Request):
    dao = UsuarioDAO(request.app.db)
    return dao.consultarUsuarioPorId(idUsuario)

# ✅ Ruta para autenticar (login) con correo y contraseña
@router.post("/autenticar", response_model=LoginRespuesta, summary="Autenticar Usuario")
def autenticar_usuario(login: LoginEntrada, request: Request):
    dao = UsuarioDAO(request.app.db)
    return dao.autenticarUsuario(login.correo, login.password)

# ✅ Ruta para registrar nuevo usuario (siempre como Cliente)
@router.post("/registrar", response_model=Salida, summary="Registrar Nuevo Usuario")
def registrar_usuario(usuario: UsuarioRegistro, request: Request):
    dao = UsuarioDAO(request.app.db)
    return dao.registrarUsuario(usuario)

# ✅ Ruta para cambiar el rol de un usuario (solo Admin debe usar esto)
@router.put("/cambiar-rol/{idUsuario}", response_model=Salida, summary="Cambiar Rol de Usuario")
def cambiar_rol_usuario(idUsuario: int, cambio: CambioRol, request: Request):
    dao = UsuarioDAO(request.app.db)
    return dao.cambiarRolUsuario(idUsuario, cambio.nuevo_rol)
