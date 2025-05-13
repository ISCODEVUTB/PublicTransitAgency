from typing import Optional
from pydantic import BaseModel

class TypeCardCreate(BaseModel):
    __entity_name__ =  "tipotarjeta"
    ID: Optional[int] = None
    Tipo: Optional[str] = None
    def to_dict(self):
        return self.model_dump()
    @classmethod
    def get_fields(cls):
        return {
            "ID": "INTEGER PRIMARY KEY",
            "Tipo": "VARCHAR(20)"
        }
class TypeCardOut(TypeCardCreate):
    __entity_name__ = "tipotarjeta"
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)