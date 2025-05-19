from App.models.CitaModel import CitaInsert, CitaDetalle, CitaCancelacion
from App.models.RespuestaModel import Salida
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from bson import ObjectId


class CitaDAO:
    def __init__(self, db):
        self.db = db

    def agendarCita(self, cita: CitaInsert) -> Salida:
        salida = Salida(estatus="", mensaje="")
        try:
            nueva_cita = jsonable_encoder(cita)
            nueva_cita["fechaRegistro"] = datetime.now()
            nueva_cita["estado"] = "Pendiente"  # ✅ campo crucial
            resultado = self.db.citas.insert_one(nueva_cita)

            salida.estatus = "OK"
            salida.mensaje = f"Cita agendada con éxito con id: {str(resultado.inserted_id)}"
        except Exception as ex:
            print("Error al agendar cita:", ex)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al agendar la cita"
        return salida

    def consultarCitaPorId(self, idCita: str) -> CitaDetalle | Salida:
        try:
            cita = self.db.citas.find_one({"_id": ObjectId(idCita)})
            if cita:
                cita["idCita"] = str(cita["_id"])
                return CitaDetalle(**cita)
            else:
                return Salida(estatus="ERROR", mensaje="Cita no encontrada")
        except Exception as ex:
            print("Error al consultar cita:", ex)
            return Salida(estatus="ERROR", mensaje="Error inesperado al consultar cita")

    def cancelarCita(self, idCita: str, cancelacion: CitaCancelacion) -> Salida:
        salida = Salida(estatus="", mensaje="")
        try:
            cita = self.db.citas.find_one({
                "_id": ObjectId(idCita),
                "estado": {"$in": ["Pendiente", "Confirmada"]}
            })

            if cita:
                resultado = self.db.citas.update_one(
                    {"_id": ObjectId(idCita)},
                    {
                        "$set": {
                            "estado": "Cancelada",
                            "motivoCancelacion": cancelacion.motivo
                        }
                    }
                )
                if resultado.modified_count == 1:
                    salida.estatus = "OK"
                    salida.mensaje = "Cita cancelada correctamente"
                else:
                    salida.estatus = "ERROR"
                    salida.mensaje = "No se pudo cancelar la cita"
            else:
                salida.estatus = "ERROR"
                salida.mensaje = "La cita no existe o ya no puede cancelarse"
        except Exception as ex:
            print("Error al cancelar cita:", ex)
            salida.estatus = "ERROR"
            salida.mensaje = "Error inesperado al cancelar la cita"
        return salida
