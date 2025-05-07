from typing import Optional
from pydantic import BaseModel

class Incidence(BaseModel):
    __entity_name__ = "incidencia"  # Nombre de la tabla en la base de datos
    id: Optional[int] = None  # Clave primaria
    idticket: Optional[int] = None  # Clave foránea al ticket
    description: Optional[str] = None  # Descripción de la incidencia
    type: Optional[str] = None  # Tipo de incidencia
    idunit: Optional[int] = None  # Clave foránea a la unidad de transporte

    def to_dict(self):
        return self.model_dump()

    @classmethod
    def get_fields(cls):
        return {
            "id": "INTEGER PRIMARY KEY",
            "idticket": "INTEGER NOT NULL",
            "description": "VARCHAR NOT NULL",
            "type": "VARCHAR NOT NULL",
            "idunit": "INTEGER NOT NULL"
        }

    @classmethod
    def ensure_table_exists(cls, cursor):
        """Verifica si la tabla existe y la crea si no existe."""
        table = cls.__entity_name__
        fields = cls.get_fields()
        columns = ", ".join(f"{k} {v}" for k, v in fields.items())
        sql = f"CREATE TABLE IF NOT EXISTS {table} ({columns})"
        cursor.execute(sql)
