prompt_classify = """Actúa como un asistente que clasifica mensajes en categorías.
    Mensaje: "{}"
    Devuelve en formato JSON con las siguientes claves:
    - categoria: tipo de actividad (entrenamiento_fuerza, entrenamiento_aerobico, habito_salud, otro)
    - confianza: valor numérico entre 0 y 1"""

prompt_search_news_system = """Eres un asistente que busca y resume noticias recientes sobre retail y supermercados en Chile."""

prompt_search_news_user = "Encuentra noticias de hoy o ayer sobre retail en Chile y entrégalas con título, fuente y resumen."