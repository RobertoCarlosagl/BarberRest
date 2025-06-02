from App.models.UsuarioModel import UsuarioSalida, LoginRespuesta, UsuarioAutenticado
from App.models.RespuestaModel import Salida

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

    def autenticarUsuario(self, correo: str, password: str) -> LoginRespuesta:
        salida = LoginRespuesta(estatus="", mensaje="", usuario=None)
        try:
            usuario = self.db.usuarios.find_one({
                "correo": correo,
                "password": password,
                "estatus": "Activo"
            })
            if usuario:
                salida.estatus = "OK"
                salida.mensaje = "Usuario autenticado"
                salida.usuario = UsuarioAutenticado(
                    idUsuario=str(usuario["_id"]),
                    nombre=usuario["nombre"],
                    correo=usuario["correo"],
                    tipo=usuario["tipo"],
                    estatus=usuario["estatus"]
                )
            else:
                salida.estatus = "ERROR"
                salida.mensaje = "Credenciales incorrectas"
        except Exception as ex:
            print("Error al autenticar:", ex)
            salida.estatus = "ERROR"
            salida.mensaje = "Error inesperado en autenticación"
        return salida