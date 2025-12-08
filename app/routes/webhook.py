from app.ai import ia_conn as ai
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import UserBase
from app.db import get_db
from app import settings
from typing import Any
from io import BytesIO
import httpx
import re
from app.utils import (
    BotWhatsApp,
    BuscadorNoticias,
    procesador_respuestas
)
from app.crud import (
    guardar_noticia,
    generar_vista_usuario,
    procesar_mensaje,
    obtener_noticia_id,
    actualizar_usuario
)


router = APIRouter(prefix="/webhook", tags=["Webhook"])

# Iniciar las clases
bot = BotWhatsApp(**settings.EVOLUTION_CREDENCIALS)
buscador = BuscadorNoticias(settings.API_KEY_NEWSAPI)

@router.post("/", include_in_schema=False) 
async def obtener_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    # 1. Obtengo el Response de parte de evolution API.
    body:dict[str, Any] = await request.json()
    
    # 2. Procesar el Response para transformarlo en modelo de Pydantic
    evolution = procesador_respuestas(body)
    texto_final = ""

    # 3. Si el Reponse  es válido, se debe seguir el flujo
    if evolution:
        # 4. Obtener el usuario a partir del Response
        usuario = await actualizar_usuario(
            db=db, 
            usuario = UserBase(
                nombre=evolution.nombre_usuario or "Sin nombre",
                numero_telefono=evolution.numero,
                permiso=True,
            )
        )

        # 5. Validar el mensaje del usuario en el caso de que sea audio o texto
        if evolution.tipo_mensaje == "audioMessage" and evolution.audio_base64:
            transcripcion = ai.transcribe_ai(evolution.audio_base64)
            texto_final = transcripcion.text.lower()
        elif evolution.tipo_mensaje == "conversation" and evolution.mensaje_texto:
            texto_final = evolution.mensaje_texto.lower()

        # 6. procesar mensaje, aca se sube toda la información del mensaje a la base de datos
        mensaje_procesado = await procesar_mensaje(
            db=db, 
            message_id=evolution.id_mensaje, 
            usuario=usuario, 
            contenido_msg=texto_final,
            tipo_mensaje=evolution.tipo_mensaje
        )
        # Si el paso anterior es verdadero, significa que el mensaje aun no ha sido resuelto
        if mensaje_procesado:
            # 7. detecta si el mensaje tiene las palabras clave
            if "busca" in texto_final and "noticias" in texto_final:
                bot.enviar_mensaje(numero=evolution.numero, mensaje=f"Hola {usuario.nombre}, buscaré noticias...", delay=1200)
                list_dict_noticias = buscador.get_news("publishedAt")

                # 8 Guarda todas las noticias que no se encuentren en la base de datos
                for dict_noticia in list_dict_noticias:
                    await guardar_noticia(session=db, data=dict_noticia, dominio_nombre=dict_noticia.dominio)

                no_vistas = await generar_vista_usuario(db=db, usuario=usuario)
                if no_vistas:
                    for n in no_vistas:
                        bot.enviar_mensaje(
                            numero=evolution.numero,
                            mensaje=f"*{n.titulo}*\n\nID de la noticia: {n.id_noticia}\n\n{n.descripcion}\n{n.url_noticia}",
                            delay=1200
                        )
                else:
                    bot.enviar_mensaje(
                        numero=evolution.numero, 
                        mensaje="no se han encontrado noticias nuevas...", 
                        delay=1200
                    )

            ids = re.findall(r"\b\d+\b", texto_final)
            if "muestra" in texto_final and ids:
                id_mensaje = int(ids[0])
                resultado = await obtener_noticia_id(db, id_mensaje)
                if resultado:
                    async with httpx.AsyncClient() as client:
                        respuesta = await client.get(resultado["imagen"])
                        foto_buffer = BytesIO(respuesta.content)
                        bot.enviar_mensaje_foto(
                            numero=evolution.numero,
                            mensaje=f"{resultado}",
                            buffer=foto_buffer,
                            delay=1200
                        )
                else:
                    bot.enviar_mensaje(
                        numero=evolution.numero,
                        mensaje="No se encuentra ese ID",
                        delay=1200
                    )
            
        await db.commit()
    else:
        pass

    # Respuesta del envio de mensajes
    return JSONResponse(content={"info": "Mensaje recibido"})