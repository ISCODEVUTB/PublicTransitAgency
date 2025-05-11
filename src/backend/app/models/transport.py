from typing import Optional
from pydantic import BaseModel

class UnidadTransporte(BaseModel):
    __entity_name__ = "UnidadTransporte"  # Nombre de la tabla en la base de datos
    Ubicacion: str
    Capacidad: int
    IDRuta: int
    IDTipo: int
    ID: Optional[str] = "EMPTY"  # Valor predeterminado según la tabla

    def to_dict(self):
        return self.dict()

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
    
    @staticmethod
    def get_fields():
        """
        Devuelve los campos de la tabla UnidadTransporte y sus tipos.
        """
        return {
            "Ubicacion": "VARCHAR(200)",
            "Capacidad": "INT",
            "IDRuta": "INT",
            "IDTipo": "INT",
            "ID": "VARCHAR(20)"
        }
