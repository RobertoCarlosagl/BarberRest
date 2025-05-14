from pydantic import BaseModel

#clase para definir el servicio de gestión de barberias con la operación de consultar barberias por su ID
class BarberiaSalida(BaseModel):
    idBarberia: str
    nombre: str
    direccion: str
    telefono: str
    estatus: str






