SELECT n.id_noticia,
       n.titulo,
       n.descripcion,
       n.url_noticia,
       n.url_imagen,
       n.fecha_publicacion,
       n.contenido
FROM noticia n
WHERE n.id_noticia NOT IN
        (SELECT un.id_noticia
         FROM usuario_noticia un
         WHERE un.id_usuario = 2);