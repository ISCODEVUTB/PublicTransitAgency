from typing import Optional
from pydantic import BaseModel, Field

class Ticket(BaseModel):
    """
    Modelo para la tabla Ticket en SQL Server.

    Campos:
    - ID: Identificador único del ticket
    - EstadoIncidencia: Estado de la incidencia del ticket
    """
    __entity_name__ = "Ticket"

    ID: int = Field(..., description="Identificador único del ticket")
    EstadoIncidencia: str = Field(..., max_length=20, description="Estado de la incidencia")

    def to_dict(self):
        return self.dict()

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    @classmethod
    def get_fields(cls):
        return {
            "ID": "INTEGER PRIMARY KEY",
            "EstadoIncidencia": "VARCHAR(20) NOT NULL"
        }
