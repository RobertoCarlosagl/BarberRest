from pydantic import BaseModel
from typing import List, Optional

#clase para definir el servicio de gestión de servicios con la operación de consultar servicios por Barberia
class ServiciosSalida(BaseModel):
    estatus: str
    mensaje: str
    servicios: Optional[List[str]] = None
