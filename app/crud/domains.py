from sqlalchemy import select
from app.models.news import Dominio
from sqlalchemy.ext.asyncio import AsyncSession


async def upsert_domain(db: AsyncSession, domain_data: dict[str, str | int]):
    """
    Inserta o actualiza una noticia según url_noticia (clave única).
    """
    stmt = select(Dominio).where(Dominio.nombre_dominio == domain_data["nombre_dominio"])
    result = await db.execute(stmt)
    noticia = result.scalar_one_or_none()

    if noticia:
        for key, value in domain_data.items():
            setattr(noticia, key, value)
    else:
        noticia = Dominio(**domain_data)
        db.add(noticia)

    await db.commit()
    await db.refresh(noticia)
    return noticia