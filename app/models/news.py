from datetime import datetime
from sqlalchemy import (
    String, Integer, Boolean, DateTime, ForeignKey
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db import Base


class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    numero_telefono: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    permiso: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

    noticias_vistas: Mapped[list["UsuarioNoticia"]] = relationship(
        back_populates="usuario", cascade="all, delete-orphan"
    )

class Noticia(Base):
    __tablename__ = "noticia"

    id_noticia: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    titulo: Mapped[str] = mapped_column(String(255), nullable=False)
    autor: Mapped[str] = mapped_column(String(100), nullable=True)
    descripcion: Mapped[str] = mapped_column(String(500), nullable=True)
    url_noticia: Mapped[str] = mapped_column(String(500), nullable=False, unique=True)
    url_imagen: Mapped[str] = mapped_column(String(500), nullable=True)
    id_dominio: Mapped[int] = mapped_column(ForeignKey("dominio.id_dominio", ondelete="CASCADE"), nullable=True)
    contenido: Mapped[str] = mapped_column(String, nullable=True)
    fecha_publicacion: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

    dominio: Mapped["Dominio"] = relationship(back_populates="noticias")
    wordpress: Mapped[list["PublicacionWordpress"]] = relationship(back_populates="noticia", cascade="all, delete-orphan")
    etiquetas: Mapped[list["NoticiaEtiqueta"]] = relationship(back_populates="noticia", cascade="all, delete-orphan")
    usuarios_vieron: Mapped[list["UsuarioNoticia"]] = relationship(back_populates="noticia", cascade="all, delete-orphan")


class PublicacionWordpress(Base):
    __tablename__ = "publicacion_wordpress"

    id_wordpress: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_noticia: Mapped[int] = mapped_column(ForeignKey("noticia.id_noticia", ondelete="CASCADE"))
    id_post_wordpress: Mapped[int] = mapped_column(Integer, unique=True)
    publicado: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

    noticia: Mapped["Noticia"] = relationship(back_populates="wordpress")


class NoticiaEtiqueta(Base):
    __tablename__ = "noticia_etiqueta"

    id_noticia_etiqueta: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_etiqueta: Mapped[int] = mapped_column(ForeignKey("etiqueta.id_etiqueta", ondelete="CASCADE"))
    id_noticia: Mapped[int] = mapped_column(ForeignKey("noticia.id_noticia", ondelete="CASCADE"))

    etiqueta: Mapped["Etiqueta"] = relationship(back_populates="noticias")
    noticia: Mapped["Noticia"] = relationship(back_populates="etiquetas")


class Etiqueta(Base):
    __tablename__ = "etiqueta"

    id_etiqueta: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre_etiqueta: Mapped[str] = mapped_column(String(100), nullable=False)
    id_etiqueta_wordpress: Mapped[int | None] = mapped_column(Integer, nullable=True)

    noticias: Mapped[list["NoticiaEtiqueta"]] = relationship(back_populates="etiqueta", cascade="all, delete-orphan")


class Dominio(Base):
    __tablename__ = "dominio"

    id_dominio: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre_dominio: Mapped[str] = mapped_column(String(255), nullable=False)
    pais: Mapped[str] = mapped_column(String(100), nullable=True)

    noticias: Mapped[list["Noticia"]] = relationship(back_populates="dominio")


class UsuarioNoticia(Base):
    __tablename__ = "usuario_noticia"

    id_usuario_noticia: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuario.id_usuario", ondelete="CASCADE"))
    id_noticia: Mapped[int] = mapped_column(ForeignKey("noticia.id_noticia", ondelete="CASCADE"))
    vista: Mapped[bool] = mapped_column(Boolean, default=False)
    fecha_vista: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

    usuario: Mapped["Usuario"] = relationship(back_populates="noticias_vistas")
    noticia: Mapped["Noticia"] = relationship(back_populates="usuarios_vieron")
