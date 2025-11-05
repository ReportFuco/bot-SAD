from pydantic import BaseModel, HttpUrl

class NoticiaBase(BaseModel):
    titulo: str
    autor:str | None = None
    descripcion: str
    url: HttpUrl
    url_imagen: HttpUrl | None = None
    contenido: str | None = None
    fecha_publicacion: str

class NoticiaCreate(NoticiaBase):
    pass

class NoticiaResponse(NoticiaBase):
    id_noticia: int
    id_dominio: int

    model_config = {
        "from_attributes": True
    }