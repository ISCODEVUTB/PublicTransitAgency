from typing import Optional
from pydantic import BaseModel, Field

class Shift(BaseModel):
    __entity_name__ = "Turno"  # Nombre de la tabla en la base de datos
    ID: Optional[int] = Field(None, description="Clave primaria")
    TipoTurno: str = Field(..., max_length=30)

    def to_dict(self):
        return self.dict()

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    @classmethod
    def get_fields(cls):
        return {
            "ID": "INTEGER PRIMARY KEY",
            "TipoTurno": "VARCHAR(30) NOT NULL"
        }
