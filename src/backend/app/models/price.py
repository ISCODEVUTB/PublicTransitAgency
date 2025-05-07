from pydantic import BaseModel

class PriceCreate(BaseModel):
    __entity_name__ = "Precio"  # <- Aquí se define el nombre general de la entidad

    ID: int
    IDTipoTransporte: int
    Monto: float

    def to_dict(self):
        return self.model_dump()
    
    @classmethod
    def get_fields(cls) -> dict:
        return {
            "ID": "INTEGER PRIMARY KEY",
            "IDTipoTransporte": "INTEGER",
            "Monto": "FLOAT"
        }
class PriceOut(PriceCreate):
    __entity_name__ = "Precio"  # <- También aquí, porque se usa para lectura

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
