from fastapi import APIRouter, Request
from App.models.CitaModel import (
    CitaInsert,             # Modelo para agendar cita
    CitaCancelacion,        # Modelo para cancelar cita
    CitaDetalle,            # Modelo de salida individual
    CitaActualizacion,      # 🆕 Modelo para actualizar cita
    HistorialVistaSalida    # Modelo de historial por usuario
)
from App.models.RespuestaModel import Salida
from App.dao.CitaDAO import CitaDAO

# Definimos el router con prefijo y categoría para Swagger
router = APIRouter(
    prefix="/citas",
    tags=["Gestión de Citas"]
)

# 🟢 Agendar cita
@router.post("", response_model=Salida, summary="Agendar Cita")
def agendar_cita(cita: CitaInsert, request: Request):
    dao = CitaDAO(request.app.db)
    return dao.agendarCita(cita)


# 🟠 Cancelar cita existente
@router.put("/{idCita}/cancelar", response_model=Salida, summary="Cancelar Cita")
def cancelar_cita(idCita: str, cancelacion: CitaCancelacion, request: Request):
    dao = CitaDAO(request.app.db)
    return dao.cancelarCita(idCita, cancelacion)

# 🔵 Consultar cita por ID
@router.get("/{idCita}", response_model=CitaDetalle | Salida, summary="Consultar Cita por ID")
def consultar_cita_por_id(idCita: str, request: Request):
    dao = CitaDAO(request.app.db)
    return dao.consultarCitaPorId(idCita)

# 🟢 Confirmar cita (cambia estado a "Confirmada")
@router.put("/{idCita}/confirmar", response_model=Salida, summary="Confirmar Cita")
def confirmar_cita(idCita: str, request: Request):
    dao = CitaDAO(request.app.db)
    return dao.confirmarCita(idCita)

# 🔍 Consultar historial de citas por usuario
@router.get("/usuario/{idUsuario}", response_model=HistorialVistaSalida, summary="Consultar Historial de Usuario")
def consultar_historial_usuario(idUsuario: int, request: Request):
    dao = CitaDAO(request.app.db)
    return dao.consultarHistorialPorUsuario(idUsuario)

# 🆕 Actualizar una cita existente
@router.put("/{idCita}", response_model=Salida, summary="Actualizar Cita")
def actualizar_cita(idCita: int, datos: CitaActualizacion, request: Request):
    dao = CitaDAO(request.app.db)
    return dao.actualizarCita(idCita, datos)
