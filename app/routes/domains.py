from fastapi import APIRouter, Depends, HTTPException
from app.schemas.domains import DomainCreate
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.crud.domains import upsert_domain
from sqlalchemy import select
from app.models.news import Dominio


router = APIRouter(prefix="/domains", tags=["Domains"])

@router.get("/")
async def leer_dominios(db:AsyncSession = Depends(get_db)):
    stmt = select(Dominio)
    result = await db.execute(stmt)
    dominios = result.scalars().all()
    return dominios

@router.get("/{domain_id}")
async def leer_dominio(domain_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(Dominio).where(Dominio.id_dominio == domain_id)
    result = await db.execute(stmt)
    dominio = result.scalar_one_or_none()
    if dominio:
        return dominio
    raise HTTPException(status_code=404, detail="Dominio no encontrado")

@router.post("/")
async def crear_dominio(domain: DomainCreate, db: AsyncSession = Depends(get_db)):
    return await upsert_domain(db, domain.model_dump())


@router.delete("/{domain_id}")
async def eliminar_dominio(domain_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(Dominio).where(Dominio.id_dominio == domain_id)
    result = await db.execute(stmt)
    dominio = result.scalar_one_or_none()
    if dominio:
        await db.delete(dominio)
        await db.commit()
        return {"message": "Dominio eliminado"}
    return HTTPException(status_code=404, detail="Dominio no encontrado")