## Mermaid asignado para el proyecto
1) se busca obtener noticias (a través de [NewsAPI](https://newsapi.org/docs) obtendrás la documentación oficial de la api) relacionadas supermercados, retail de chile como en el mundo.

2) Una vez hecho la extracción de noticias, el usaurio debe decidir cual será publicada en el sitio [Supermercados al día](https://supermercadoaldia.cl) para que luego el agente realice la mejora de redacción y posteriormente subida al sitio.
***
representado de la siguiente manera:

```mermaid
erDiagram

    usuario {
        int id_usuario PK
        string numero_telefono UK
        string nombre
        bool permiso
        datetime created_at
    }

    noticia {
        int id_noticia PK
        string titulo
        string autor
        string descripcion
        string url_noticia UK
        string url_imagen
        string id_dominio FK
        datetime fecha_publicacion
    }

    publicacion_wordpress {
        int id_publicacion PK
        int id_noticia FK
        int id_post_wordpress UK
        bool publicado
        string url_publicacion
        datetime fecha_publicacion
    }
    

    noticia_etiqueta {
        int id_noticia_etiqueta PK
        int id_etiqueta FK
        int id_noticia FK
    }
    etiqueta {
        int id_etiqueta PK
        string nombre_etiqueta
        int id_etiqueta_wordpress
    }

    usuario_noticia {
        int id_usuario_noticia PK
        int id_usuario FK
        int id_noticia FK
        bool vista
    }

    dominio {
        int id_dominio PK
        string nombre_dominio
        string pais
    }

    %% relaciones

    usuario ||--o{usuario_noticia:"revisa"
    noticia ||--o{usuario_noticia:"tiene"
    etiqueta ||--o{noticia_etiqueta:"asigna"
    noticia ||--o{noticia_etiqueta:"posee"
    dominio ||--o{noticia: "tiene"
    noticia ||--|| publicacion_wordpress: "estado"
    
```

## Dato importante
- los datos conciderados en el siguiente esquema entidad relación están pensados para interactuar con los diferentes requerimientos dentro del proyecto