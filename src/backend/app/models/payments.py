from typing import Optional
from pydantic import BaseModel

class Payment(BaseModel):
    """
    Modelo para la tabla Pago en SQL Server.

    Campos:
    - IDMovimiento: Clave foránea a la tabla Movimiento
    - IDPago: Clave foránea a la tabla Precio
    - IDTarjeta: Clave foránea a la tabla Tarjeta
    - IDTransporte: Clave foránea a la tabla UnidadTransporte
    """
    __entity_name__ = "Pago"

    IDMovimiento: int
    IDPago: int
    IDTarjeta: int
    IDTransporte: int

    def to_dict(self):
        """
        Serializa el modelo `Payment` en un diccionario.
        """
        return self.dict()

    @classmethod
    def get_fields(cls):
        """
        Define los campos de la tabla para su creación.
        """
        return {
            "IDMovimiento": "INTEGER NOT NULL",
            "IDPago": "INTEGER NOT NULL",
            "IDTarjeta": "INTEGER NOT NULL",
            "IDTransporte": "INTEGER NOT NULL"
        }
