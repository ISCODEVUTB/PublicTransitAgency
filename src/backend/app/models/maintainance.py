from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class MaintenanceCreate(BaseModel):
    __entity_name__ = "mantenimientoins"
    
    ID: Optional[int] = None
    id_status: Optional[int] = None
    type: Optional[str] = None
    fecha: Optional[datetime] = None
    idunidad: Optional[int] = None
    
    def to_dict(self):
        """Convierte el objeto a un diccionario"""
        return self.model_dump()

    @classmethod
    def get_fields(cls):
        """Devuelve los campos de la tabla como un diccionario con los tipos de datos"""
        return {
            "ID": "INTEGER PRIMARY KEY",       # ID de la entidad, clave primaria
            "id_status":"INTEGER",                # ID del estado (entero)
            "type": "varchar(100)",                    # Tipo de mantenimiento (cadena de texto)
            "fecha": "DATE",                    # Fecha del mantenimiento (type DATE)
            "idunidad": "INTEGER",              # ID de la unidad asociada (entero)
        }
class MaintenanceOut(MaintenanceCreate):
    __entity_name__ = "mantenimientoins"
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)