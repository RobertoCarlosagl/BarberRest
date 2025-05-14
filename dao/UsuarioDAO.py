from models.UsuarioModel import UsuarioSalida
from models.RespuestaModel import Salida

class UsuarioDAO:
    def __init__(self, db):
        self.db = db

    def consultarUsuarioPorId(self, idUsuario: str) -> UsuarioSalida | Salida:
        try:
            # Convertimos el id recibido en string a int, ya que en Mongo se guardó como número
            usuario = self.db.usuarios.find_one({"_id": int(idUsuario)})

            if usuario:
                usuario["idUsuario"] = str(usuario["_id"])  # para que encaje con el modelo
                return UsuarioSalida(**usuario)
            else:
                return Salida(estatus="ERROR", mensaje="Usuario no encontrado")
        except Exception as e:
            print("Error al consultar usuario:", e)
            return Salida(estatus="ERROR", mensaje="Error inesperado al consultar usuario")
