from bson import ObjectId
from models.UsuarioModel import UsuarioSalida
from models.RespuestaModel import Salida

class UsuarioDAO:
    def __init__(self, db):
        self.db = db

    # Clase para definir el servicio Gestión de usuarios con la operación de consultar Usario por ID
    def consultarUsuarioPorId(self, idUsuario: str) -> UsuarioSalida | Salida:
        try:
            usuario = self.db.usuarios.find_one({"_id": ObjectId(idUsuario)})
            if usuario:
                usuario["idUsuario"] = str(usuario["_id"])
                return UsuarioSalida(**usuario)
            else:
                return Salida(estatus="ERROR", mensaje="Usuario no encontrado")
        except Exception as ex:
            print("Error al consultar usuario:", ex)
            return Salida(estatus="ERROR", mensaje="Error al consultar usuario")
