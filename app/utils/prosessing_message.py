from typing import Any
from app.schemas import ResponseBaseModel


def procesador_respuestas(body: dict[str, Any]) -> ResponseBaseModel | None:
    data: dict[str, Any] = body.get("data", {})

    key_data = data.get("key", {})

    number: str = key_data.get("remoteJid", "").replace("@s.whatsapp.net", "")
    msg_id: str = key_data.get("id", "")
    push_name = data.get("pushName", None)

    if data:
        message_type: str = data.get("messageType", "No encontrado")
        message_data = data.get("message", {})

        if message_type == "conversation":
            message = message_data.get("conversation", "sin mensaje")
            return ResponseBaseModel(
                numero=number, 
                tipo_mensaje=message_type, 
                mensaje_texto=message, 
                id_mensaje=msg_id,
                nombre_usuario=push_name
            )

        elif message_type == "audioMessage":
            audio_message = message_data.get("base64", "")
            return ResponseBaseModel(
                numero=number, 
                tipo_mensaje=message_type, 
                audio_base64=audio_message, 
                id_mensaje=msg_id,
                nombre_usuario=push_name
            )

        return ResponseBaseModel(
            numero=number, 
            tipo_mensaje=message_type, 
            id_mensaje=msg_id
        )

    # Caso sin data
    return None
