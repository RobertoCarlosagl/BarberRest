from fastapi import APIRouter, Request
from App.dao.BarberoDAO import BarberoDAO
from App.models.BarberoModel import BarberosVistaSalida, BarberoSalida

router = APIRouter(prefix="/barberos", tags=["Barberos"])

# Consultar todos los barberos por ID de barbería
@router.get("/por-barberia/{idBarberia}", response_model=BarberosVistaSalida)
def consultar_barberos_por_barberia(idBarberia: int, request: Request):
    dao = BarberoDAO(request.app.db)
    return dao.consultarBarberosPorBarberia(idBarberia)

# Consultar un barbero específico por su ID
@router.get("/{idBarbero}", response_model=BarberoSalida)
def consultar_barbero_por_id(idBarbero: int, request: Request):
    dao = BarberoDAO(request.app.db)
    return dao.consultarBarberoPorId(idBarbero)
