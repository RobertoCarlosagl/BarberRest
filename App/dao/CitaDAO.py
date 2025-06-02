from App.models.CitaModel import CitaInsert, CitaDetalle, CitaCancelacion, HistorialVistaSalida, HistorialVistaCita
from App.models.RespuestaModel import Salida
from fastapi.encoders import jsonable_encoder
from datetime import datetime


class CitaDAO:
    def __init__(self, db):
        self.db = db

    def agendarCita(self, cita: CitaInsert) -> Salida:
        salida = Salida(estatus="", mensaje="")
        try:
            nueva_cita = jsonable_encoder(cita)
            nueva_cita["_id"] = self.db.citas.count_documents({}) + 200  # ejemplo simple
            nueva_cita["fechaRegistro"] = datetime.now()
            nueva_cita["estado"] = "Pendiente"

            resultado = self.db.citas.insert_one(nueva_cita)

            salida.estatus = "OK"
            salida.mensaje = f"Cita agendada con éxito con id: {str(nueva_cita['_id'])}"
        except Exception as ex:
            print("Error al agendar cita:", ex)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al agendar la cita"
        return salida

    def consultarCitaPorId(self, idCita: str) -> CitaDetalle | Salida:
        try:
            cita = self.db.citas.find_one({"_id": int(idCita)})
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
                "_id": int(idCita),
                "estado": {"$in": ["Pendiente", "Confirmada"]}
            })

            if cita:
                resultado = self.db.citas.update_one(
                    {"_id": int(idCita)},
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

    def confirmarCita(self, idCita: str) -> Salida:
        salida = Salida(estatus="", mensaje="")
        try:
            cita = self.db.citas.find_one({
                "_id": int(idCita),
                "estado": {"$in": ["Pendiente", "Agendada"]}
            })

            if cita:
                resultado = self.db.citas.update_one(
                    {"_id": int(idCita)},
                    {"$set": {"estado": "Confirmada"}}
                )
                if resultado.modified_count == 1:
                    salida.estatus = "OK"
                    salida.mensaje = "Cita confirmada correctamente"
                else:
                    salida.estatus = "ERROR"
                    salida.mensaje = "No se pudo confirmar la cita"
            else:
                salida.estatus = "ERROR"
                salida.mensaje = "La cita no existe o no puede confirmarse"
        except Exception as ex:
            print("Error al confirmar cita:", ex)
            salida.estatus = "ERROR"
            salida.mensaje = "Error inesperado al confirmar cita"
        return salida

    def consultarHistorialPorUsuario(self, idUsuario: int) -> HistorialVistaSalida:
        salida = HistorialVistaSalida(estatus="", mensaje="", historial=[])
        try:
            historial = list(self.db.historialUsuarioView.find({"idCliente": idUsuario}))
            if historial:
                for cita in historial:
                    cita["idCita"] = str(cita["idCita"])
                salida.estatus = "OK"
                salida.mensaje = "Historial encontrado desde vista"
                salida.historial = historial
            else:
                salida.estatus = "ERROR"
                salida.mensaje = "No hay citas para este usuario"
        except Exception as e:
            print("Error:", e)
            salida.estatus = "ERROR"
            salida.mensaje = "Error inesperado"
        return salida
