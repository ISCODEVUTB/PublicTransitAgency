from typing import Optional
from pydantic import BaseModel

class Incidence(BaseModel):
    """
    Modelo para la tabla Incidencia en SQL Server.

    Campos:
    - ID: Identificador único de la incidencia
    - IDTicket: Clave foránea al ticket
    - Descripcion: Descripción de la incidencia
    - Tipo: Tipo de incidencia
    - IDUnidad: Clave foránea a la unidad de transporte (VARCHAR)
    """
    __entity_name__ = "Incidencia"

    ID: Optional[int] = None
    IDTicket: Optional[int] = None
    Descripcion: Optional[str] = None
    Tipo: Optional[str] = None
    IDUnidad: Optional[str] = None  # Cambiado a str

    def to_dict(self):
        return self.dict()

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
    
    @classmethod
    def get_fields(cls):
        """
        Define los campos de la tabla para su creación.
        """
        return {
            "ID": "INTEGER PRIMARY KEY",
            "IDTicket": "INTEGER NOT NULL",
            "Descripcion": "VARCHAR(255) NOT NULL",
            "Tipo": "VARCHAR(50) NOT NULL",
            "IDUnidad": "VARCHAR(50) NOT NULL"  # Cambiado a VARCHAR(50)
        }

