from App.models.CitaModel import CitaInsert, CitaDetalle, CitaCancelacion, HistorialVistaSalida, HistorialVistaCita
from App.models.CitaModel import CitaActualizacion
from App.models.RespuestaModel import Salida
from fastapi.encoders import jsonable_encoder
from datetime import datetime, date, time



class CitaDAO:
    def __init__(self, db):
        self.db = db

    def agendarCita(self, cita: CitaInsert) -> Salida:
        salida = Salida(estatus="", mensaje="")
        errores = []

        # Validar que el cliente exista y esté activo
        cliente = self.db.usuarios.find_one({
            "idUsuario": cita.idCliente,
            "tipo": "Cliente",
            "estatus": "Activo"
        })
        if not cliente:
            errores.append("ID de cliente inválido o no está activo.")

        # Validar que el barbero exista en la colección barberos
        barbero = self.db.barberos.find_one({
            "idBarbero": cita.idBarbero
        })
        if not barbero:
            errores.append("ID de barbero inválido.")

        # Validar que la fecha no sea pasada
        if cita.fecha < date.today():
            errores.append("No se puede agendar una cita en una fecha pasada.")

        # Validar que los servicios existan
        if not cita.servicios or not isinstance(cita.servicios, list):
            errores.append("Debe proporcionar al menos un servicio.")
        else:
            for servicio_id in cita.servicios:
                if not self.db.servicios.find_one({"_id": int(servicio_id)}):
                    errores.append(f"Servicio con ID {servicio_id} no existe.")
                    break

        # Si hay errores, los devolvemos todos
        if errores:
            salida.estatus = "ERROR"
            salida.mensaje = " | ".join(errores)
            return salida

        # Verificar conflicto de horario con ese barbero
        conflicto = self.db.citas.find_one({
            "idBarbero": cita.idBarbero,
            "fecha": datetime.combine(cita.fecha, cita.hora),
            #"hora": cita.hora,
            "estado": {"$in": ["Pendiente", "Confirmada"]}
        })
        if conflicto:
            salida.estatus = "ERROR"
            salida.mensaje = "El barbero ya tiene una cita en ese horario."
            return salida

        # Insertar la cita
        nueva_cita = jsonable_encoder(cita)
        nueva_cita["_id"] = self.db.citas.count_documents({}) + 200
        nueva_cita["fecha"] = datetime.combine(cita.fecha, cita.hora)  # 👈 Mongo friendly
        nueva_cita["fechaRegistro"] = datetime.now()
        nueva_cita["estado"] = "Pendiente"

        self.db.citas.insert_one(nueva_cita)

        salida.estatus = "OK"
        salida.mensaje = "Cita agendada exitosamente."
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

    def actualizarCita(self, idCita: int, datos: CitaActualizacion) -> Salida:
        salida = Salida(estatus="", mensaje="")
        try:
            # Verificar si la cita existe
            cita = self.db.citas.find_one({"_id": idCita})
            if not cita:
                salida.estatus = "ERROR"
                salida.mensaje = "La cita no existe"
                return salida

            # Validar que el barbero exista y esté activo
            barbero = self.db.usuarios.find_one({
                "_id": datos.idBarbero,
                "estatus": "Activo",
                "tipo": "Barbero"
            })
            if not barbero:
                salida.estatus = "ERROR"
                salida.mensaje = "El barbero no existe o no está activo"
                return salida

            # Validar conflicto de horario para ese barbero
            conflicto = self.db.citas.find_one({
                "_id": {"$ne": idCita},
                "idBarbero": datos.idBarbero,
                "fecha": datos.fecha,
                "hora": datos.hora,
                "estado": {"$in": ["Pendiente", "Confirmada"]}
            })
            if conflicto:
                salida.estatus = "ERROR"
                salida.mensaje = "Ese horario ya está ocupado para el barbero"
                return salida

            # Realizamos la actualización
            self.db.citas.update_one(
                {"_id": idCita},
                {"$set": {
                    "idBarbero": datos.idBarbero,
                    "fecha": datos.fecha,
                    "hora": datos.hora,
                    "servicios": datos.servicios
                }}
            )

            salida.estatus = "OK"
            salida.mensaje = "Cita actualizada correctamente"
        except Exception as ex:
            print("Error al actualizar cita:", ex)
            salida.estatus = "ERROR"
            salida.mensaje = "Error inesperado al actualizar la cita"
        return salida
