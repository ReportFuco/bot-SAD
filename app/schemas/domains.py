from pydantic import BaseModel, Field


class DomainBase(BaseModel):
    nombre_dominio: str = Field(..., max_length=255)
    pais: str | None = Field(None, max_length=100)


class DomainCreate(DomainBase):
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "nombre_dominio": "supermercadosaldia.cl",
                "pais": "Chile"
            }
        }
    }

class DomainResponse(DomainBase):
    id_dominio: int
    model_config = {
        "from_attributes": True,
    }