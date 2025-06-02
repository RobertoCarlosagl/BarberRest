from App.models.BarberoModel import BarberosVistaSalida, BarberoVista, BarberoSalida

class BarberoDAO:
    def __init__(self, db):
        self.db = db

    def consultarBarberosPorBarberia(self, idBarberia: int) -> BarberosVistaSalida:
        salida = BarberosVistaSalida(estatus="", mensaje="", barberos=[])
        try:
            # Paso 1: buscar el nombre de la barbería
            barberia = self.db.barberias.find_one({"_id": idBarberia})
            if not barberia:
                salida.estatus = "ERROR"
                salida.mensaje = "Barbería no encontrada"
                return salida

            nombre_barberia = barberia["nombre"]

            # Paso 2: buscar en la vista por ese nombre
            barberos = list(self.db.barberosview.find({"barberia.nombre": nombre_barberia}))

            if barberos:
                salida.estatus = "OK"
                salida.mensaje = "Barberos encontrados"
                salida.barberos = [BarberoVista(**b) for b in barberos]
            else:
                salida.estatus = "ERROR"
                salida.mensaje = "No hay barberos en esta barbería"
        except Exception as e:
            print("Error:", e)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al consultar barberos por barbería"
        return salida

    def consultarBarberoPorId(self, idBarbero: int) -> BarberoSalida:
        salida = BarberoSalida(estatus="", mensaje="", barbero=None)
        try:
            barbero = self.db.barberosview.find_one({"idBarbero": idBarbero})
            if barbero:
                salida.estatus = "OK"
                salida.mensaje = "Barbero encontrado"
                salida.barbero = BarberoVista(**barbero)
            else:
                salida.estatus = "ERROR"
                salida.mensaje = "Barbero no encontrado"
        except Exception as e:
            print("Error:", e)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al consultar barbero por ID"
        return salida


