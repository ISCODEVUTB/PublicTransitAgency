from typing import Optional
from pydantic import BaseModel

class Payment(BaseModel):
    __entity_name__ = "pago"
    id: Optional[int] = None  # Clave primaria
    iduser: Optional[int] = None  # ID del usuario
    amount: Optional[float] = None  # Monto del pago
    idmovement: Optional[int] = None  # ID del movimiento
    idtransportunit: Optional[int] = None  # ID de la unidad de transporte
    idcard: Optional[int] = None  # ID de la tarjeta

    def to_dict(self):
        return self.model_dump()

    @classmethod
    def get_fields(cls):
        return {
            "id": "INTEGER PRIMARY KEY",
            "iduser": "INTEGER NOT NULL",
            "amount": "FLOAT NOT NULL",
            "idmovement": "INTEGER NOT NULL",
            "idtransportunit": "INTEGER NOT NULL",
            "idcard": "INTEGER NOT NULL"
        }
