from typing import Optional
from pydantic import BaseModel

class CardCreate(BaseModel):
    __entity_name__ = "tarjeta"
    ID: Optional[int] = None
    IDUsuario: Optional[int] = None
    IDTipoTarjeta: Optional[int] = None
    Saldo: Optional[int] = None

    def to_dict(self):
        return self.model_dump()

    @classmethod
    def get_fields(cls)-> dict:
        return {
            "ID": "INTEGER PRIMARY KEY",       # ID como clave primaria
            "IDUsuario": "INTEGER",            # IDUsuario como entero
            "IDTipoTarjeta": "INTEGER",        # IDTipoTarjeta como entero
            "Saldo": "INTEGER"                   # Saldo como número decimal (REAL)
        }

class CardOut(CardCreate):
    __entity_name__ = "tarjeta"
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
