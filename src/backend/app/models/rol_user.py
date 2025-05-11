from pydantic import BaseModel

class RolUserCreate(BaseModel):
    __entity_name__ =  "RolUsuario"  # <- Aquí se define el nombre general de la entidad
    ID: int
    Rol: str

    def to_dict(self):
        return self.model_dump()

    @classmethod
    def get_fields(cls) -> dict:
        return {
            "ID": "INTEGER PRIMARY KEY",
            "Rol": "varchar(20)",
        }
class RolUserOut(RolUserCreate):
    __entity_name__ = "RolUsuario"  # <- También aquí, porque se usa para lectura
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
