from models.ServicioModel import ServiciosSalida
from bson import ObjectId

class ServicioDAO:
    def __init__(self, db):
        self.db = db

    #logica para definir el servicio de gestión de servicios con la operación de consultar servicios por Barberia
    def consultarServiciosPorBarberia(self, idBarberia: str) -> ServiciosSalida:
        salida = ServiciosSalida(estatus="", mensaje="", servicios=[])
        try:
            servicios = list(self.db.servicios.find(
                {"idBarberia": ObjectId(idBarberia)},
                {"_id": 0, "tipo": 1}
            ))
            if servicios:
                salida.estatus = "OK"
                salida.mensaje = "Servicios encontrados"
                salida.servicios = [s["tipo"] for s in servicios if "tipo" in s]
            else:
                salida.estatus = "ERROR"
                salida.mensaje = "No se encontraron servicios para esta barbería"
        except Exception as ex:
            print("Error al consultar servicios:", ex)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al consultar los servicios"
        return salida
