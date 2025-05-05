from typing import Optional
from pydantic import BaseModel

class Transport(BaseModel):
    __entity_name__ = "unidadtransporte"
    id: Optional[int] = None
    idtype: Optional[int] = None
    status: Optional[str] = None
    ubication: Optional[str]     = None
    capacity: Optional[int] = None

    def to_dict(self):
        return self.model_dump()

    @classmethod
    def get_fields(cls):
        return {
            "id": "INTEGER PRIMARY KEY",
            "idtype": "INTEGER",
            "status": "TEXT",
            "ubication": "TEXT",
            "capacity": "INTEGER"
        }