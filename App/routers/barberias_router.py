from fastapi import APIRouter, Request
from App.dao.BarberiaDAO import BarberiaDAO
from App.models.BarberiaModel import BarberiaSalida
from App.models.RespuestaModel import Salida

router = APIRouter(prefix="/barberias", tags=["Barberías"])

#ruta para definir el servicio de gestión de barberias con la operación de consultar barberias por su ID
@router.get("/{idBarberia}", response_model=BarberiaSalida | Salida)
def consultar_barberia_por_id(idBarberia: str, request: Request):
    dao = BarberiaDAO(request.app.db)
    return dao.consultarBarberiaPorId(idBarberia)
