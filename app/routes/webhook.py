from app.crud import (
    guardar_noticia, generar_vista_usuario, 
    procesar_mensaje, obtener_noticia_id, actualizar_usuario
)
from app.utils import BotWhatsApp, BuscadorNoticias, procesador_respuestas
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


# Iniciar el Router de FastAPI
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
                noticias = buscador.get_news(sort_by="publishedAt", q="unimarc")
                noticias_2 = buscador.get_news(sort_by="publishedAt", q="supermercados")
                noticias_3 = buscador.get_news(sort_by="publishedAt", q="retail")
                noticias_4 = buscador.get_news(sort_by="publishedAt", q="industria")
                noticias_5 = buscador.get_news(sort_by="publishedAt", q="mercado internacional")
                list_dict_noticias = noticias + noticias_2 + noticias_3 + noticias_4 + noticias_5

                # 8 Guarda todas las noticias que no se encuentren en la base de datos
                for dict_noticia in list_dict_noticias:
                    await guardar_noticia(session=db, data=dict_noticia, dominio_nombre=dict_noticia.dominio)

                # 9. Extraer las noticias que no ha visto el usuario
                no_vistas = await generar_vista_usuario(db=db, usuario=usuario)
                if no_vistas:
                    # 10. Enviar noticias que no ha visto el usuario
                    for n in no_vistas:
                        bot.enviar_mensaje(
                            numero=evolution.numero,
                            mensaje=f"*{n.titulo}*\n\nID de la noticia: {n.id_noticia}\n\n{n.descripcion}\n{n.url_noticia}",
                            delay=1200
                        )
                else:
                    # 11. Enviar mensaje si no encuentra noticias nuevas
                    bot.enviar_mensaje(
                        numero=evolution.numero, 
                        mensaje="no se han encontrado noticias nuevas...", 
                        delay=1200
                    )

            # 12. Segundo caso: buscar por ID de noticia
            ids = re.findall(r"\b\d+\b", texto_final)
            if "muestra" in texto_final and ids:
                id_mensaje = int(ids[0])
                resultado = await obtener_noticia_id(db, id_mensaje)

                if resultado:
                    try:
                        async with httpx.AsyncClient() as client:
                            respuesta = await client.get(resultado["imagen"])
                        
                        # Validar contenido de imagen (200 OK + no vacío)
                        if respuesta.status_code == 200 and respuesta.content:
                            foto_buffer = BytesIO(respuesta.content)
                            bot.enviar_mensaje_foto(
                                numero=evolution.numero,
                                mensaje=f"{resultado}",
                                buffer=foto_buffer,
                                delay=1200
                            )
                        else:
                            # Si la imagen no sirve
                            bot.enviar_mensaje(
                                numero=evolution.numero,
                                mensaje=f"Encontré la noticia, pero no tiene imagen disponible.\n🔎 ID: {id_mensaje}",
                                delay=1200
                            )

                    except Exception as e:
                        # ❗ Cualquier error de red, URL inválida, timeout, etc.
                        bot.enviar_mensaje(
                            numero=evolution.numero,
                            mensaje=f"Encontré la noticia, pero hubo un error al cargar la imagen.\n🔎 ID: {id_mensaje} - {e}",
                            delay=1200
                        )

                else:
                    bot.enviar_mensaje(
                        numero=evolution.numero,
                        mensaje="No se encuentra ese ID",
                        delay=1200
                    )


        # Observaciones, el programa genera error al enviar la noticia ID si es que no cuenta con foto válida
        await db.commit()
    else:
        pass

    # Respuesta del envio de mensajes
    return JSONResponse(content={"info": "Mensaje recibido"})