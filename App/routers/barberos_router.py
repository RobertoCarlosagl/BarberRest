from fastapi import APIRouter, Request
from App.models.BarberoModel import BarberosVistaSalida, BarberoSalida
from App.dao.BarberoDAO import BarberoDAO

router = APIRouter(prefix="/barberos", tags=["Gestión de Barberos"])

@router.get(
    "/por-barberia/{idBarberia}",
    response_model=BarberosVistaSalida,
    summary="Consultar Barberos Por Barbería"
)
def get_barberos_por_barberia(idBarberia: int, request: Request):
    db = request.app.db
    dao = BarberoDAO(db)
    return dao.consultarBarberosPorBarberia(idBarberia)

@router.get(
    "/{idBarbero}",
    response_model=BarberoSalida,
    summary="Consultar Barbero Por ID"
)
def get_barbero_por_id(idBarbero: int, request: Request):
    db = request.app.db
    dao = BarberoDAO(db)
    return dao.consultarBarberoPorId(idBarbero)
