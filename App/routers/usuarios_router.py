from fastapi import APIRouter, Request
from App.dao.UsuarioDAO import UsuarioDAO
from App.models.UsuarioModel import UsuarioSalida, LoginEntrada, LoginRespuesta
from App.models.RespuestaModel import Salida
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


