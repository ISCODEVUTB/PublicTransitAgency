from pydantic import BaseModel
class UserCreate(BaseModel):
    __entity_name__ = "Usuario"  # <- Aquí se define el nombre general de la entidad
    ID: int
    Identificacion: int
    Nombre: str
    Apellido: str
    Correo: str
    Contrasena: str
    IDRolUsuario: int
    IDTurno: int
    IDTarjeta: int

    def to_dict(self):
        return self.model_dump()
        
    @classmethod
    def get_fields(cls) -> dict:
        return {
            "ID": "INTEGER PRIMARY KEY",
            "Identificacion": "INTEGER",
            "Nombre": "VARCHAR(100)",
            "Apellido": "VARCHAR(100)",
            "Correo": "VARCHAR(100)",
            "Contrasena": "VARCHAR(100)",
            "IDRolUsuario": "INTEGER",
            "IDTurno": "INTEGER",
            "IDTarjeta": "INTEGER",
        }
class UserOut(UserCreate):
    __entity_name__ = "Usuario"  # <- También aquí, porque se usa para lectura

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)