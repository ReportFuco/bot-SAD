from app.ai import ia_conn as ai
from app.utils.whatsapp import BotWhatsApp
from app.utils.buscador_noticias import BuscadorNoticias
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.crud.operations import guardar_noticia
from app import settings
from typing import Any

from app.utils import (
    prosessing_message as pm, 
    # wp_conn as wp
)

router = APIRouter(prefix="/webhook", tags=["Webhook"])

# Iniciar las clases
bot = BotWhatsApp(**settings.EVOLUTION_CREDENCIALS)
buscador = BuscadorNoticias(settings.API_KEY_NEWSAPI)

@router.post("/", include_in_schema=False)
async def obtener_webhook(request: Request):
    body:dict[str, Any] = await request.json()
    
    number_user, msg_type, message = pm.prosesing_requests(body)

    if msg_type == "audioMessage":
        transcripcion = ai.transcribe_ai(message)
        
        if "busca" in transcripcion.text and "noticias" in transcripcion.text:
            # Enviar mensaje de vuelta por WhatsApp
            bot.enviar_mensaje(numero=number_user, mensaje=transcripcion.text, delay=1200)

            dict_noticias = buscador.get_news("publishedAt")
            

    elif msg_type == "conversation":

        # Flujo del usuario diga la frase clave
        if "busca" in message and "noticias" in message:
            buscador.get_news(bot, number_user)

    # Respuesta del envio de mensajes
    return JSONResponse(content={"info": "Mensaje recibido"})