from pydantic import BaseModel
from datetime import datetime
from app.schemas.domains import DomainResponse

class NoticiaBase(BaseModel):
    titulo: str
    autor:str | None = None
    descripcion: str
    url_noticia: str
    url_imagen: str | None = None
    contenido: str | None = None
    id_dominio: DomainResponse
    fecha_publicacion: datetime

class NoticiaCreate(NoticiaBase):
    pass

class NoticiaResponse(NoticiaBase):
    id_noticia: int
    id_dominio: int

    model_config = {
        "from_attributes": True
    }