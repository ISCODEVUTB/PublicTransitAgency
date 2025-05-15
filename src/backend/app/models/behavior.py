from pydantic import BaseModel
import datetime
class BehaviorCreate(BaseModel):
    __entity_name__ = "Rendimiento"  # <- Aquí se define el nombre general de la entidad
    ID: int
    cantidadrutas: int
    horastrabajadas: int
    observaciones:str
    fecha:str
    iduser:int

    def to_dict(self):
        return self.model_dump()
        
    @classmethod
    def get_fields(cls) -> dict:
        return {
            "ID": "INTEGER PRIMARY KEY",
            "cantidadrutas": "INTEGER",
            "horastrabajadas": "INTEGER",
            "observaciones": "VARCHAR",
            "fecha": "DATE",
            "iduser":"INTEGER"
        }
class BehaviorOut(BehaviorCreate):
    __entity_name__ = "Rendimiento"  # <- También aquí, porque se usa para lectura

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)