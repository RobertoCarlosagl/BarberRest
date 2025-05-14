from pydantic import BaseModel
from datetime import date, time
from typing import List
from typing import Optional

#CLase para definir la operación de Agendar Cita
class CitaInsert(BaseModel):
    idCliente: int
    idBarbero: int
    fecha: date
    hora: time
    servicios: List[str]

class Salida(BaseModel):
    estatus: str
    mensaje: str


#Clase para definir la operación de cancelar cita
class CitaCancelacion(BaseModel):
    motivo: str

#Clase para definir la operación de consultar cita por ID
class CitaDetalle(BaseModel):
    idCita: str
    idCliente: int
    idBarbero: int
    fecha: date
    hora: time
    estado: str
    servicios: List[str]
    motivoCancelacion: Optional[str] = None
