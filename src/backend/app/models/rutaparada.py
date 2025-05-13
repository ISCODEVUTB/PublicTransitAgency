from pydantic import BaseModel

class RutaParada(BaseModel):
    IDRuta: int
    IDParada: int

    __entity_name__ = "RutaParada"

    @staticmethod
    def get_fields():
        return {
            "IDRuta": "INT NOT NULL",
            "IDParada": "INT NOT NULL",
        }

    def to_dict(self):
        return self.dict()