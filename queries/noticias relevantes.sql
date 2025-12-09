SELECT 
    n.id_noticia,
    n.titulo,
    n.descripcion,
    n.fecha_publicacion,
    d.nombre_dominio,
    ts_rank_cd(
        -- Pesos: A es más fuerte que B, C, D
        setweight(to_tsvector('spanish', n.titulo), 'A') ||
        setweight(to_tsvector('spanish', n.contenido), 'B') ||
        setweight(to_tsvector('spanish', d.nombre_dominio), 'A'),
        to_tsquery('spanish', 'retail | supermercado | unimarc | lider | cadena | consumo | chile')
    ) AS relevancia
FROM noticia n
JOIN dominio d ON n.id_dominio = d.id_dominio
WHERE 
    (
        setweight(to_tsvector('spanish', n.titulo), 'A') ||
        setweight(to_tsvector('spanish', n.contenido), 'B') ||
        setweight(to_tsvector('spanish', d.nombre_dominio), 'A')
    ) @@ to_tsquery('spanish', 'retail | supermercado | unimarc | lider | cadena | consumo | chile')
ORDER BY relevancia DESC, fecha_publicacion DESC;
