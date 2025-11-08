from pydantic import BaseModel
from datetime import datetime
from app.schemas.domains import DomainResponse

class NoticiaBase(BaseModel):
    titulo: str
    autor: str | None = None
    descripcion: str
    url_noticia: str
    url_imagen: str | None = None
    contenido: str | None = None
    fecha_publicacion: datetime | None = None

class NoticiaCreate(NoticiaBase):
    id_dominio: int

    model_config = {
        "json_schema_extra": {
            "example": {
                "titulo": "Lanzamiento nuevo local",
                "autor": "Francisco Arancibia",
                "descripcion": "Supermercados al Día abre una nueva sucursal en Viña del Mar.",
                "url_noticia": "https://supermercadosaldia.cl/nueva-sucursal-vina",
                "url_imagen": "https://supermercadosaldia.cl/img/nueva.jpg",
                "contenido": "La empresa continúa su expansión en la región...",
                "id_dominio": 1
            }
        }
    }

class NoticiaResponse(NoticiaBase):
    id_noticia: int
    dominio: DomainResponse | None = None

    model_config = {
        "from_attributes": True
    }
