from app.models import Usuario
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.users import UserBase


async def actualizar_usuario(db:AsyncSession, usuario: UserBase)-> Usuario:
    buscar_usuario = await db.execute(
        select(Usuario).where(
            Usuario.numero_telefono == usuario.numero_telefono
        )
    )
    usuario_encontrado = buscar_usuario.scalar_one_or_none()

    if usuario_encontrado:
        return usuario_encontrado
    else:
        registrar_usuario = Usuario(
            numero_telefono=usuario.numero_telefono,
            nombre=usuario.nombre,
            permiso=True,
        )
        db.add(registrar_usuario)

        return registrar_usuario