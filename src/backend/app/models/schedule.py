from typing import Optional
from pydantic import BaseModel, Field

class Schedule(BaseModel):
    """
    Modelo para la tabla Horario en SQL Server.

    Campos:
    - ID: Identificador único del horario
    - Llegada: Hora de llegada
    - Salida: Hora de salida
    """
    __entity_name__ = "horario"  # Nombre de la tabla en la base de datos

    ID: int = Field(..., description="Identificador único del horario")
    Llegada: str = Field(..., description="Hora de llegada (formato TIME)")
    Salida: str = Field(..., description="Hora de salida (formato TIME)")

    def to_dict(self):
        return self.dict()

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    @classmethod
    def get_fields(cls):
        return {
            "ID": "INTEGER PRIMARY KEY",
            "Llegada": "TIME NOT NULL",
            "Salida": "TIME NOT NULL"
        }