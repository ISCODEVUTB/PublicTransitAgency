from pydantic import BaseModel

class TypeMovementCreate(BaseModel):
    __entity_name__ = "TipoMovimiento"  # <- Aquí se define el nombre general de la entidad
    ID: int
    TipoMovimiento: str

    def to_dict(self):
        return self.model_dump()
    @classmethod
    def get_fields(cls) -> dict:
        return {
            "ID": "INTEGER PRIMARY KEY",
            "TipoMovimiento": "varchar(20)",
        }
class TypeMovementOut(TypeMovementCreate):
    __entity_name__ = "TipoMovimiento"  # <- También aquí, porque se usa para lectura
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
