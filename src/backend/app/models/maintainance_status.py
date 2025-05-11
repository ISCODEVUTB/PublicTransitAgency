from typing import Optional
from pydantic import BaseModel, Field

class MaintainanceStatus(BaseModel):
    """
    Modelo para la tabla EstadoMantenimiento en SQL Server.

    Campos:
    - ID: Identificador único del estado de mantenimiento
    - TipoEstado: Tipo de estado de mantenimiento
    """
    __entity_name__ = "EstadoMantenimiento"

    ID: int = Field(..., description="Identificador único del estado de mantenimiento")
    TipoEstado: str = Field(..., max_length=100, description="Tipo de estado de mantenimiento")

    def to_dict(self):
        return self.dict()

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
    
    @classmethod
    def get_fields(cls):
        return {
            "ID": "int NOT NULL PRIMARY KEY",
            "TipoEstado": "varchar(100) NOT NULL"
        }
