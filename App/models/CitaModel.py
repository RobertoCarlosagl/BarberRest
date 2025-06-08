from pydantic import BaseModel
from datetime import date, time
from typing import List, Optional

# Clase para definir la operación de agendar una cita
class CitaInsert(BaseModel):
    idCliente: int
    idBarbero: int
    fecha: date
    hora: time
    servicios: List[int]  # ✅ ahora acepta IDs numéricos

# Clase para cancelar una cita
class CitaCancelacion(BaseModel):
    motivo: str

# Clase para consultar cita por ID
class CitaDetalle(BaseModel):
    idCita: str
    idCliente: int
    idBarbero: int
    fecha: date
    hora: time
    estado: str
    servicios: List[int]  # ✅ corregido también aquí
    motivoCancelacion: Optional[str] = None

# Clase opcional si decides registrar quién confirma
class CitaConfirmacion(BaseModel):
    confirmadoPor: str

# Vista individual del historial del cliente
class HistorialVistaCita(BaseModel):
    idCita: int
    fecha: str
    hora: str
    estado: str
    servicios: List[int]

# Salida del historial completo
class HistorialVistaSalida(BaseModel):
    estatus: str
    mensaje: str
    historial: List[HistorialVistaCita]

# Clase para actualizar una cita existente
class CitaActualizacion(BaseModel):
    idBarbero: int
    fecha: date
    hora: time
    servicios: List[int]  # ✅ también aquí
