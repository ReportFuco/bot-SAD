from pydantic import BaseModel
from datetime import datetime
from app.schemas.domains import DomainResponse

class NoticiaBase(BaseModel):
    titulo: str
    autor: str | None
    descripcion: str
    url_noticia: str
    url_imagen: str | None
    contenido: str | None
    dominio: str | None
    fecha_publicacion: datetime | None

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
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id_noticia": 12,
                "titulo": "Supermercados al Día inaugura nueva sucursal en Viña del Mar",
                "autor": "Francisco Arancibia",
                "descripcion": "La empresa continúa su expansión en la región de Valparaíso.",
                "url_noticia": "https://supermercadosaldia.cl/nueva-sucursal-vina",
                "url_imagen": "https://supermercadosaldia.cl/img/nueva.jpg",
                "contenido": "Con una inversión de más de $500 millones, la empresa busca fortalecer su presencia en la zona costera...",
                "fecha_publicacion": "2025-11-09T12:00:00Z",
                "dominio": {
                    "id_dominio": 1,
                    "nombre_dominio": "supermercadosaldia.cl",
                    "pais": "Chile"
                }
            }
        }
    }