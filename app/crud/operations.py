from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.news import Usuario


async def obtener_info_numero(db: AsyncSession, numero_telefono: str):
    stmt = select(Usuario).where(Usuario.numero_telefono == numero_telefono)
    result = await db.execute(stmt)
    usuario = result.scalar_one_or_none()
    return usuario