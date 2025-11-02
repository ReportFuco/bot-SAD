from app.ai import prompts
from base64 import b64decode
from openai import OpenAI
from app.settings import API_KEY_OPENAI
import json
import re
import io


client = OpenAI(api_key=API_KEY_OPENAI)

def transcribe_ai(base64:str):
    """
    Funcion para transcribir de Audios a Texto

    parametros:
        base64 -> Audio pasado a formato Base64 (Entregado por Evolution API)

    retornos:
        audio transcrito a texto.
    """
    audio_bytes = b64decode(base64)
    audio_buffer = io.BytesIO(audio_bytes)

    audio_buffer.name = "audio.ogg"

    return client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_buffer
    )


def search_news()->str:
    response = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {"role": "system", "content": prompts.prompt_search_news_system},
            { "role": "user", "content":  prompts.prompt_search_news_user}

        ]
    )
    return response.choices[0].message.content or "{}"


def classify_message(message: str) -> dict[str, str | float]:
    """
    Funcion para clasificar texto con OpenAI:
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres un clasificador de mensajes de hábitos y entrenamientos."},
            {"role": "user", "content": prompts.prompt_classify.format(message)}
        ],
        temperature=0.2,
    )

    content:str = response.choices[0].message.content or "{}"
    content = re.sub(r"^```(json)?|```$", "", content.strip()).strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:

        return {"categoria": "otro", "confianza": 0.0}