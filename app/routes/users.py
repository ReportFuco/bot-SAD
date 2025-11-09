from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.news import Usuario
from app.schemas.users import UserCreate
from app.db import get_db
from sqlalchemy import select


router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
async def read_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Usuario))
    users = result.scalars().all()
    return users

@router.get("/{user_id}")
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Usuario).where(Usuario.id_usuario == user_id))
    user = result.scalar_one_or_none()
    if user:
        return user
    return HTTPException(status_code=404, detail="Usuario no encontrado")

@router.post("/create")
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(
        select(Usuario).where(Usuario.numero_telefono == user.numero_telefono)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=409,
            detail=f"El usuario con número de teléfono '{user.numero_telefono}' ya existe."
        )

    nuevo_usuario = Usuario(
        numero_telefono=user.numero_telefono.title(),
        nombre=user.nombre,
        permiso=user.permiso
    )
    db.add(nuevo_usuario)
    await db.commit()
    await db.refresh(nuevo_usuario)
    return nuevo_usuario