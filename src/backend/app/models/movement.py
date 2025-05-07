from pydantic import BaseModel

class MovementCreate(BaseModel):
    __entity_name__ =  "Movimiento"  # <- Aquí se define el nombre general de la entidad
    ID: int
    IDTipoMovimiento: int
    Monto: float

    def to_dict(self):
        return self.model_dump()
    
    @classmethod
    def get_fields(cls) -> dict:
        return {
            "ID": "INTEGER PRIMARY KEY",
            "IDTipoMovimiento": "INTEGER",
            "Monto": "FLOAT"
        }

class MovementOut(MovementCreate):
    __entity_name__ = "Movimiento"  # <- También aquí, porque se usa para lectura
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
