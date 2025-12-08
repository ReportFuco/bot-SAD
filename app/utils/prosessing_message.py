from typing import Any, Tuple

def prosesing_requests(body: dict[str, Any]) -> Tuple[str, str, str, str]:
    data: dict[str, Any] = body.get("data", {})

    key_data = data.get("key", {})

    number: str = key_data.get("remoteJid", "")
    msg_id: str = key_data.get("id", "")

    if data:
        message_type: str = data.get("messageType", "No encontrado")
        message_data = data.get("message", {})

        if message_type == "conversation":
            message = message_data.get("conversation", "sin mensaje")
            return (number, message_type, message, msg_id)

        elif message_type == "audioMessage":
            audio_message = message_data.get("base64", "")
            return (number, message_type, audio_message, msg_id)

        # Si no es conversation ni audioMessage
        return (number, message_type, "Sin mensaje", msg_id)

    # Caso sin data
    return ("sin numero", "No data", "Sin mensaje", "Sin ID")
