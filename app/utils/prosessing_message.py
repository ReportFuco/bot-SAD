from typing import Any, Tuple

def prosesing_requests(body: dict[str, Any]) -> Tuple[str, str, str]:
    data: dict[str, Any] = body.get("data", {})

    number:str  = data.get("key", "").get("remoteJid", "")

    if data:
        message_type: str = data.get("messageType", "No encontrado")

        if message_type == "conversation":
            message = data.get("message", {}).get("conversation", "sin mensaje")
            return (number, message_type, message)

        elif message_type == "audioMessage":
            audio_message = data.get("message", {}).get("base64")
            return (number, message_type, audio_message)

        return (number, message_type, "Sin mensaje")
    
    # Caso sin data
    return ("sin numero", "No data", "Sin mensaje")