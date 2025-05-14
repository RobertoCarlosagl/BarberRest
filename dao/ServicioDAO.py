from models.ServicioModel import ServiciosSalida

class ServicioDAO:
    def __init__(self, db):
        self.db = db

    def consultarServiciosPorBarberia(self, idBarberia: str) -> ServiciosSalida:
        salida = ServiciosSalida(estatus="", mensaje="", servicios=[])
        try:
            # Cambiamos "idBarberia" a "barberia_id" para que coincida con tu JSON
            servicios = list(self.db.servicios.find({"barberia_id": int(idBarberia)}))

            if servicios:
                salida.estatus = "OK"
                salida.mensaje = "Servicios encontrados"
                salida.servicios = [s["nombre"] for s in servicios if "nombre" in s]
            else:
                salida.estatus = "ERROR"
                salida.mensaje = "No se encontraron servicios para esta barbería"
        except Exception as ex:
            print("Error al consultar servicios:", ex)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al consultar los servicios"
        return salida
