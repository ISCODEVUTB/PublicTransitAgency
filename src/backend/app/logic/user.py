import re
from card import Card
from pydantic import BaseModel
class User:
    def __init__(self, id_user: int, type_identification: str, identification: int ,name: str, email: str, password: str, role: str, card: Card):
        self.id_user = id_user
        self.type_identification = type_identification
        self.identification = identification
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.card = card

    
    @property
    def information(self):
            return(f"Information:\n"
                   f"\tID:{self.id_user}\n"
                   f"\tType of Identification: {self.type_identification}\n"
                   f"\tIdentification: {self.identification}\n"
                   f"\tName: {self.name}\n"
                   f"\tEmail: {self.email}\n"
                   f"\tPassword: {self.password}\n"
                   f"\tRole: {self.role}")
    
    def update_information(self, attribute, value):
        match attribute.lower():
            case "name":
                if not self.verify_name(value):
                    raise ValueError("Invalid Name")
                self.name = value
            case "email":
                if not self.verify_email(value):
                    raise ValueError("Invalid Email")
                self.email = value
            case "password":
                if not self.verify_password(value):
                    raise ValueError("Invalid Password")
            case _:
                raise ValueError("Not a Valid Attribute")

    def verify_information(self, attribute, value):
        match attribute.lower():
            case "name":
                if not self.verify_name(value):
                    raise ValueError("Invalid Name")
                self.name = value
            case "email":
                if not self.verify_email(value):
                    raise ValueError("Invalid Email")
                self.email = value
            case "password":
                if not self.verify_password(value):
                    raise ValueError("Invalid Password")
                self.password = value
            case _:
                raise ValueError("Not a Valid Attribute")

    @staticmethod
    def verify_name(value):
        """Valida que el nombre solo contenga letras y espacios, sin múltiples espacios consecutivos"""
        return bool(re.match(r"^[A-Za-z]+(?:\s[A-Za-z]+)*$", value))

    @staticmethod
    def verify_email(value):
        """Valida que el email tenga un formato correcto"""
        return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", value))

    @staticmethod
    def verify_password(value):
        """Valida que la contraseña tenga al menos 6 caracteres, un número y un carácter especial"""
        return bool(re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$", value))
        
    def use_card(self):
        raise NotImplementedError("The user method must be implemented by subclasses.")
    
    def assign_card(self, card):
        self.card = card

class UserCreate(BaseModel):
    __entity_name__ = "user"  # <- Aquí se define el nombre general de la entidad
    id: int
    identification: int
    name: str
    lastname: str
    email: str
    password: str
    idtype_user: int
    idturn: int

    def to_dict(self):
        return self.dict()

class UserOut(UserCreate):
    __entity_name__ = "user"  # <- También aquí, porque se usa para lectura

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)