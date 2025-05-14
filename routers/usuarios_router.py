from fastapi import APIRouter, Request
from dao.UsuarioDAO import UsuarioDAO
from models.UsuarioModel import UsuarioSalida
from models.RespuestaModel import Salida
router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


#ruta para consultar usuario por su ID
@router.get("/{idUsuario}", response_model=UsuarioSalida | Salida)
def consultar_usuario_por_id(idUsuario: str, request: Request):
    dao = UsuarioDAO(request.app.db)
    return dao.consultarUsuarioPorId(idUsuario)
