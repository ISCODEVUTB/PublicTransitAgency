from typing import Optional
from pydantic import BaseModel

class RutaParada(BaseModel):
    __entity_name__ = "rutaparada"  # Nombre de la tabla en la base de datos

    IDParada: Optional[int] = None  # Clave foránea a la tabla ruta
    IDRuta: Optional[int] = None  # Clave foránea a la tabla parada

    def to_dict(self):
        """
        Serializa el modelo `RutaParada` en un diccionario.
        """
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: dict):
        """
        Crea una instancia de `RutaParada` a partir de un diccionario.
        """
        return cls(**data)

    @classmethod
    def get_fields(cls):
        """
        Define los campos de la tabla para su creación.
        """
        return {
            "IDParada": "INTEGER NOT NULL",
            "IDRuta": "INTEGER NOT NULL"
        }