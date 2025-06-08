from App.models.UsuarioModel import UsuarioSalida, LoginRespuesta, UsuarioAutenticado
from App.models.RespuestaModel import Salida
from App.models.UsuarioModel import UsuarioRegistro  # Asegúrate de tener este modelo importado
from App.models.RespuestaModel import Salida

class UsuarioDAO:
    def __init__(self, db):
        self.db = db

    def consultarUsuarioPorId(self, idUsuario: str) -> UsuarioSalida | Salida:
        try:
            usuario = self.db.usuarios.find_one({"idUsuario": int(idUsuario)})
            if usuario:
                usuario["idUsuario"] = str(usuario["idUsuario"])  # 👈 esta línea soluciona todo
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

    # Método para registrar un nuevo usuario (solo tipo Cliente)
    def registrarUsuario(self, datos: UsuarioRegistro) -> Salida:
        salida = Salida(estatus="", mensaje="")
        try:
            # Verificar si ya existe un usuario con el mismo correo
            existe = self.db.usuarios.find_one({"correo": datos.correo})
            if existe:
                salida.estatus = "ERROR"
                salida.mensaje = "El correo ya está registrado"
                return salida

            # Generar ID nuevo de forma incremental
            nuevo_id = self.db.usuarios.count_documents({}) + 1

            # Convertimos el modelo recibido a diccionario y completamos los datos
            usuario = datos.dict()
            usuario["_id"] = nuevo_id
            usuario["idUsuario"] = nuevo_id
            usuario["tipo"] = "Cliente"  # Forzamos el tipo
            usuario["estatus"] = "Activo"  # Estatus por default

            # Insertamos el nuevo usuario
            self.db.usuarios.insert_one(usuario)

            salida.estatus = "OK"
            salida.mensaje = f"Usuario registrado con ID {nuevo_id}"
        except Exception as e:
            print("Error al registrar usuario:", e)
            salida.estatus = "ERROR"
            salida.mensaje = "No se pudo registrar el usuario"
        return salida

    # Método para cambiar el rol de un usuario (solo a Admin o Barbero)
    def cambiarRolUsuario(self, idUsuario: int, nuevo_rol: str) -> Salida:
        salida = Salida(estatus="", mensaje="")
        try:
            # Validamos que el nuevo rol sea válido
            if nuevo_rol not in ["Admin", "Barbero"]:
                salida.estatus = "ERROR"
                salida.mensaje = "Rol inválido. Solo se permite Admin o Barbero."
                return salida

            # Intentamos actualizar el rol
            resultado = self.db.usuarios.update_one(
                {"_id": idUsuario},
                {"$set": {"tipo": nuevo_rol}}
            )

            if resultado.modified_count == 1:
                salida.estatus = "OK"
                salida.mensaje = f"Rol cambiado correctamente a {nuevo_rol}"
            else:
                salida.estatus = "ERROR"
                salida.mensaje = "No se encontró el usuario o ya tenía ese rol"
        except Exception as e:
            print("Error al cambiar rol:", e)
            salida.estatus = "ERROR"
            salida.mensaje = "Error interno al cambiar rol"
        return salida