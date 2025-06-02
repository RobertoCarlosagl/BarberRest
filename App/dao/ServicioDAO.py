from App.models.ServicioModel import ServiciosSalida, Servicio, ServicioSalida

class ServicioDAO:
    def __init__(self, db):
        self.db = db

    def consultarServiciosPorBarberia(self, idBarberia: int) -> ServiciosSalida:
        salida = ServiciosSalida(estatus="", mensaje="", servicios=[])
        try:
            servicios = list(self.db.servicios.find({"barberia_id": idBarberia}))

            if servicios:
                for s in servicios:
                    s["idServicio"] = s["_id"]
                salida.estatus = "OK"
                salida.mensaje = "Servicios encontrados"
                salida.servicios = [Servicio(**s) for s in servicios]
            else:
                salida.estatus = "ERROR"
                salida.mensaje = "No se encontraron servicios para esta barbería"
        except Exception as ex:
            print("Error al consultar servicios:", ex)
            salida.estatus = "ERROR"
            salida.mensaje = "Error inesperado al consultar servicios"
        return salida

    def consultarServicioPorId(self, idServicio: int) -> ServicioSalida:
        salida = ServicioSalida(estatus="", mensaje="", servicio=None)
        try:
            servicio = self.db.servicios.find_one({"_id": idServicio})
            if servicio:
                servicio["idServicio"] = servicio["_id"]
                salida.estatus = "OK"
                salida.mensaje = "Servicio encontrado"
                salida.servicio = Servicio(**servicio)
            else:
                salida.estatus = "ERROR"
                salida.mensaje = "Servicio no encontrado"
        except Exception as e:
            print("Error al consultar servicio:", e)
            salida.estatus = "ERROR"
            salida.mensaje = "Error inesperado al consultar servicio"
        return salida