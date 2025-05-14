from bson import ObjectId
from models.BarberiaModel import BarberiaSalida
from models.RespuestaModel import Salida

class BarberiaDAO:
    def __init__(self, db):
        self.db = db

    #logica para definir el servicio de gestión de barberias con la operación de consultar barberias por su ID
    def consultarBarberiaPorId(self, idBarberia: str) -> BarberiaSalida | Salida:
        try:
            barberia = self.db.barberias.find_one({"_id": ObjectId(idBarberia)})
            if barberia:
                barberia["idBarberia"] = str(barberia["_id"])
                return BarberiaSalida(**barberia)
            else:
                return Salida(estatus="ERROR", mensaje="Barbería no encontrada")
        except Exception as ex:
            print("Error al consultar barbería:", ex)
            return Salida(estatus="ERROR", mensaje="Error al consultar la barbería")
