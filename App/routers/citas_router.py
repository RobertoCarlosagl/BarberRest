from fastapi import APIRouter, Request
from App.models.CitaModel import CitaInsert, CitaCancelacion, CitaDetalle, HistorialVistaSalida
from App.models.RespuestaModel import Salida
from App.dao.CitaDAO import CitaDAO

router = APIRouter(prefix="/citas", tags=["Citas"])

#Ruta para la opración de agendar cita
@router.post("", response_model=Salida)
def agendar_cita(cita: CitaInsert, request: Request) -> Salida:
    dao = CitaDAO(request.app.db)
    return dao.agendarCita(cita)

#Ruta para la opración de cancelar cita
@router.put("/{idCita}/cancelar", response_model=Salida)
def cancelar_cita(idCita: str, cancelacion: CitaCancelacion, request: Request) -> Salida:
    dao = CitaDAO(request.app.db)
    return dao.cancelarCita(idCita, cancelacion)

#Ruta para la operación de consuiltar cita por su ID
@router.get("/{idCita}", response_model=CitaDetalle | Salida)
def consultar_cita_por_id(idCita: str, request: Request):
    dao = CitaDAO(request.app.db)
    return dao.consultarCitaPorId(idCita)

@router.put("/{idCita}/confirmar", response_model=Salida)
def confirmar_cita(idCita: str, request: Request):
    dao = CitaDAO(request.app.db)
    return dao.confirmarCita(idCita)

@router.get("/usuario/{idUsuario}", response_model=HistorialVistaSalida)
def consultar_historial_usuario(idUsuario: int, request: Request):
    dao = CitaDAO(request.app.db)
    return dao.consultarHistorialPorUsuario(idUsuario)
