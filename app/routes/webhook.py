from app.utils.whatsapp import BotWhatsApp
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app import settings
from typing import Any

from app.utils import (
    ia_conn as ai, 
    prosessing_message as pm, 
    # wp_conn as wp
)

router = APIRouter(prefix="/webhook", tags=["Webhook"])

bot = BotWhatsApp(**settings.EVOLUTION_CREDENCIALS)

@router.post("/")
async def obtener_webhook(request: Request):
    body:dict[str, Any] = await request.json()
    
    user, number_user, msg_type, message = pm.prosesing_requests(body)

    if msg_type == "audioMessage":
        transcripcion = ai.transcribe_ai(message)
        print(f"INFO:     Usuario: {user}.")
        print(f"INFO:     Mensaje transcrito: {transcripcion.text}")

        # Enviar mensaje de vuelta por WhatsApp
        bot.enviar_mensaje(numero=number_user, mensaje=transcripcion.text, delay=1200)
        
        clasificacion = ai.classify_message(transcripcion.text)
        print(f"INFO:     Clasificación: {clasificacion['categoria']}")
    elif msg_type == "conversation":
        clasificacion = ai.classify_message(message)
        print(f"INFO:     Usuario: {user}.")
        print(f"INFO:     Mensaje: {message}.")
        print(f"INFO:     Clasificación: {clasificacion['categoria']}")

        # Enviar mensaje del usuario por WhatsApp
        bot.enviar_mensaje(numero=number_user, mensaje=message, delay=1200)
    
    # Respuesta del envio de mensajes
    return JSONResponse(content={"info": "Mensaje recibido"})