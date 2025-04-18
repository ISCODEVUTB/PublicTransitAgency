from pydantic import BaseModel

class RolUserCreate(BaseModel):
    __entity_name__ =  "roluser"
    id: int
    tipo: str

    def to_dict(self):
        return self.dict()

class RolUserOut(RolUserCreate):
    __entity_name__ = "roluser"
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
