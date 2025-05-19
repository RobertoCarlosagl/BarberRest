from fastapi import APIRouter, Request
from App.dao.ServicioDAO import ServicioDAO
from App.models.ServicioModel import ServiciosSalida

router = APIRouter(prefix="/barberias", tags=["Servicios"])

#ruta para definir el servicio de gestión de servicios con la operación de consultar servicios por Barberia
@router.get("/{idBarberia}/servicios", response_model=ServiciosSalida)
def consultar_servicios_por_barberia(idBarberia: str, request: Request):
    dao = ServicioDAO(request.app.db)
    return dao.consultarServiciosPorBarberia(idBarberia)


