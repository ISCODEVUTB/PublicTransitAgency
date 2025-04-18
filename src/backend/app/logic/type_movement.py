from pydantic import BaseModel

class TypeMovementCreate(BaseModel):
    __entity_name__ = "typemovement"
    id: int
    tipo: str

    def to_dict(self):
        return self.dict()

class TypeMovementOut(TypeMovementCreate):
    __entity_name__ = "typemovement"
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
