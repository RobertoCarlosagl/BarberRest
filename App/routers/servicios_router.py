from fastapi import APIRouter, Request
from App.dao.ServicioDAO import ServicioDAO
from App.models.ServicioModel import ServiciosSalida, ServicioSalida

router = APIRouter(prefix="/servicios", tags=["Servicios"])

# Obtener todos los servicios de una barbería por su ID
@router.get("/por-barberia/{idBarberia}", response_model=ServiciosSalida)
def consultar_servicios_por_barberia(idBarberia: int, request: Request):
    dao = ServicioDAO(request.app.db)
    return dao.consultarServiciosPorBarberia(idBarberia)

# Obtener un servicio específico por su ID
@router.get("/{idServicio}", response_model=ServicioSalida)
def consultar_servicio_por_id(idServicio: int, request: Request):
    dao = ServicioDAO(request.app.db)
    return dao.consultarServicioPorId(idServicio)
