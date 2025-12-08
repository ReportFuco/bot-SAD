from app.ai import ia_conn as ai
from app.utils.whatsapp import BotWhatsApp
from app.utils.buscador_noticias import BuscadorNoticias
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app import settings
from typing import Any
from io import BytesIO
import httpx
from app.crud.news import obtener_noticia_id
from app.crud.operations import (
    guardar_noticia,
    generar_vista_usuario,
    prosesing_message
)
import re
from app.utils import (
    prosessing_message as pm, 
    # wp_conn as wp
)

router = APIRouter(prefix="/webhook", tags=["Webhook"])

# Iniciar las clases
bot = BotWhatsApp(**settings.EVOLUTION_CREDENCIALS)
buscador = BuscadorNoticias(settings.API_KEY_NEWSAPI)

@router.post("/", include_in_schema=False) 
async def obtener_webhook(
    request: Request, 
    db: AsyncSession = Depends(get_db)
):
    
    body:dict[str, Any] = await request.json()
    
    number_user, msg_type, message, msg_id = pm.prosesing_requests(body)
    number_user = number_user.replace("@s.whatsapp.net", "")
    texto_final = ""

    if msg_type == "audioMessage":
        transcripcion = ai.transcribe_ai(message)
        texto_final = transcripcion.text.lower()

    elif msg_type == "conversation":
        texto_final = message.lower()

    mensaje_procesado = await prosesing_message(
        db=db, 
        message_id=msg_id, 
        numero=number_user, 
        contenido_msg=texto_final
    )
    # Primer comando realizado
    if mensaje_procesado:
        if "busca" in texto_final and "noticias" in texto_final:
            bot.enviar_mensaje(numero=number_user, mensaje=f"Buscando noticias...", delay=1200)
            list_dict_noticias = buscador.get_news("publishedAt")

            for dict_noticia in list_dict_noticias:
                await guardar_noticia(session=db, data=dict_noticia, dominio_nombre=dict_noticia.dominio)

            no_vistas = await generar_vista_usuario(db, number_user)
            if no_vistas:
                for n in no_vistas:
                    bot.enviar_mensaje(
                        numero=number_user,
                        mensaje=f"*{n.titulo}*\n\nID de la noticia: {n.id_noticia}\n\n{n.descripcion}\n{n.url_noticia}",
                        delay=1200
                    )
            else:
                bot.enviar_mensaje(
                    numero=number_user, 
                    mensaje="no se han encontrado noticias nuevas...", 
                    delay=1200
                )

        if "muestra" in texto_final and f"{re.findall(r'\b\d+\b', texto_final)[0]}" in texto_final:
            id_mensaje = int(re.findall(r'\b\d+\b', texto_final)[0])

            resultado = await obtener_noticia_id(db, id_mensaje)
            if resultado:
                async with httpx.AsyncClient() as client:
                    respuesta = await client.get(resultado["imagen"])
                    foto_buffer = BytesIO(respuesta.content)
                    bot.enviar_mensaje_foto(
                        numero=number_user,
                        mensaje=f"{resultado}",
                        buffer=foto_buffer,
                        delay=1200
                    )
            else:
                bot.enviar_mensaje(
                    numero=number_user,
                    mensaje="No se encuentra ese ID",
                    delay=1200
                )
        
    await db.commit()

    # Respuesta del envio de mensajes
    return JSONResponse(content={"info": "Mensaje recibido"})