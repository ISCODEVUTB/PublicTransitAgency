from typing import Optional
from pydantic import BaseModel

class Parada(BaseModel):
    __entity_name__ = "Parada"  

    ID: Optional[int] = None  
    Ubicacion: str  
    Nombre: str  

    def to_dict(self):
        """
        Serializa el modelo `Parada` en un diccionario.
        """
        return self.dict()

    @classmethod
    def from_dict(cls, data: dict):
        """
        Crea una instancia de `Parada` a partir de un diccionario.
        """
        return cls(**data)

    @classmethod
    def get_fields(cls):
        """
        Define los campos de la tabla para su creación.
        """
        return {
            "ID": "INT PRIMARY KEY",
            "Ubicacion": "VARCHAR NOT NULL",
            "Nombre": "VARCHAR NOT NULL"
        }
