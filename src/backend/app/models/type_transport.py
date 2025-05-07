from pydantic import BaseModel

class TypeTransportCreate(BaseModel):
    __entity_name__ =  "TipoTransporte"  # <- Aquí se define el nombre general de la entidad
    ID: int
    TipoTransporte: str

    def to_dict(self):
        return self.model_dump()
    
    @classmethod
    def get_fields(cls) -> dict:
        return {
            "ID": "INTEGER PRIMARY KEY",
            "TipoTransporte": "varchar(20)",
        }

class TypeTransportOut(TypeTransportCreate):
    __entity_name__ = "TipoTransporte"  # <- También aquí, porque se usa para lectura
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
