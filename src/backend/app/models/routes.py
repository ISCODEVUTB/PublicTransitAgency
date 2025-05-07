from typing import Optional
from pydantic import BaseModel

class Route(BaseModel):
    __entity_name__ = "ruta"  # Nombre de la tabla en la base de datos

    id: Optional[int] = None  # Clave primaria
    idhorario: int  # Clave foránea a la tabla Horario
    name: str  # Nombre de la ruta

    def to_dict(self):
        """
        Serializa el modelo `Route` en un diccionario.
        """
        return self.model_dump()

    @classmethod
    def get_fields(cls):
        """
        Define los campos de la tabla para su creación.
        """
        return {
            "id": "INT PRIMARY KEY",
            "idhorario": "INT NOT NULL",
            "name": "VARCHAR(255) NOT NULL"
        }
