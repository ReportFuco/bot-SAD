from pydantic import BaseModel


class UserBase(BaseModel):
    nombre: str
    permiso: bool = False
    numero_telefono: str


class UserCreate(UserBase):

    def max_length_numero_telefono(cls) -> int:
        return 11
    
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "nombre": "Juan Perez",
                "permiso": False,
                "numero_telefono": "56912345678"
            }
        }
    }

class UserResponse(UserBase):
    id_usuario: int

    model_config = {
        "from_attributes": True,
    }