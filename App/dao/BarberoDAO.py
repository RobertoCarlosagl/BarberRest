from App.models.BarberoModel import (
    BarberoVista,
    BarberosVistaSalida,
    BarberoSalida
)


class BarberoDAO:
    def __init__(self, db):
        self.db = db

    def consultarBarberosPorBarberia(self, idBarberia: int) -> BarberosVistaSalida:
        salida = BarberosVistaSalida(estatus="", mensaje="", barberos=[])
        try:
            resultado = list(self.db.barberos.find({"idBarberia": idBarberia}))
            barberos_validos = []

            for b in resultado:
                usuario = self.db.usuarios.find_one({
                    "idUsuario": b["idUsuario"],
                    "tipo": "Barbero"
                })
                barberia = self.db.barberias.find_one({"_id": b["idBarberia"]})

                if usuario and barberia:
                    barbero_data = {
                        "idBarbero": b["idBarbero"],
                        "especialidad": b["especialidad"],
                        "horario": b["horario"],
                        "usuario": {
                            "nombre": usuario["nombre"],
                            "correo": usuario["correo"],
                            "telefono": usuario["telefono"],
                            "tipo": usuario["tipo"]
                        },
                        "barberia": {
                            "nombre": barberia["nombre"],
                            "direccion": barberia["direccion"]
                        }
                    }
                    barberos_validos.append(barbero_data)

            if barberos_validos:
                salida.estatus = "OK"
                salida.mensaje = "Barberos encontrados"
                salida.barberos = [BarberoVista(**b) for b in barberos_validos]
            else:
                salida.estatus = "ERROR"
                salida.mensaje = "No hay barberos en esta barbería"
        except Exception as ex:
            print("Error al consultar barberos por barbería:", ex)
            salida.estatus = "ERROR"
            salida.mensaje = "Error inesperado al consultar barberos"
        return salida

    def consultarBarberoPorId(self, idBarbero: int) -> BarberoSalida:
        salida = BarberoSalida(estatus="", mensaje="", barbero=None)
        try:
            barbero = self.db.barberos.find_one({"idBarbero": idBarbero})
            if not barbero:
                salida.estatus = "ERROR"
                salida.mensaje = "Barbero no encontrado"
                return salida

            usuario = self.db.usuarios.find_one({
                "idUsuario": barbero["idUsuario"],
                "tipo": "Barbero"
            })
            barberia = self.db.barberias.find_one({"_id": barbero["idBarberia"]})

            if usuario and barberia:
                data = {
                    "idBarbero": barbero["idBarbero"],
                    "especialidad": barbero["especialidad"],
                    "horario": barbero["horario"],
                    "usuario": {
                        "nombre": usuario["nombre"],
                        "correo": usuario["correo"],
                        "telefono": usuario["telefono"],
                        "tipo": usuario["tipo"]
                    },
                    "barberia": {
                        "nombre": barberia["nombre"],
                        "direccion": barberia["direccion"]
                    }
                }
                salida.estatus = "OK"
                salida.mensaje = "Barbero encontrado"
                salida.barbero = BarberoVista(**data)
            else:
                salida.estatus = "ERROR"
                salida.mensaje = "No es un barbero válido"
        except Exception as e:
            print("Error al consultar barbero por ID:", e)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al consultar barbero por ID"
        return salida
