from pydantic import BaseModel
import datetime
class PQRCreate(BaseModel):
    __entity_name__ = "pqr"  # <- Aquí se define el nombre general de la entidad
    id: int
    type: str
    description: str
    fecha: str
    identificationuser: int

    def to_dict(self):
        return self.model_dump()
        
    @classmethod
    def get_fields(cls) -> dict:
        return {
            "id": "INTEGER PRIMARY KEY",
            "type": "VARCHAR",
            "description": "VARCHAR",
            "fecha": "DATE",
            "identificationuser": "INTEGER"
        }
class PQROut(PQRCreate):
    __entity_name__ = "pqr"  # <- También aquí, porque se usa para lectura

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)