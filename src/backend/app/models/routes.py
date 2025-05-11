from typing import Optional
from pydantic import BaseModel

class Route(BaseModel):
    __entity_name__ = "Rutas"  # Nombre de la tabla en la base de datos

    ID: Optional[int] = None  # Clave primaria
    IDHorario: int  # Clave foránea a la tabla Horario
    Nombre: str  # Nombre de la ruta

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
            "ID": "INT PRIMARY KEY",
            "IDHorario": "INT NOT NULL",
            "Nombre": "VARCHAR(255) NOT NULL"
        }
