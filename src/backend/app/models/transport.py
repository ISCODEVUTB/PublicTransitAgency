from typing import Optional
from pydantic import BaseModel

class Transport(BaseModel):
    """
    Modelo para la tabla UnidadTransporte.
    """
    __entity_name__ = "UnidadTransporte"

    ID: Optional[int] = None  # Clave primaria autoincremental
    Ubicacion: str  # Ubicación de la unidad
    Capacidad: int  # Capacidad de la unidad
    IDRuta: int  # Clave foránea a la tabla Ruta
    IDTipo: int  # Clave foránea a la tabla Tipo

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
            "ID": "INT IDENTITY(1,1) PRIMARY KEY",
            "Ubicacion": "VARCHAR(200) NOT NULL",
            "Capacidad": "INT NOT NULL",
            "IDRuta": "INT NOT NULL",
            "IDTipo": "INT NOT NULL"
        }

