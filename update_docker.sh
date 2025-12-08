#!/bin/bash

# Script para automatizar la actualización de contenedores Docker Compose
# Autor: Francisco

set -e

cd "$(dirname "$0")"

echo "=========================================="
echo "  🚀 Actualización de contenedores Docker"
echo "  Fecha: $(date)"
echo "=========================================="

# 1️⃣ Detener contenedores del proyecto
echo "🛑 Deteniendo contenedores del proyecto..."
docker compose down

# 2️⃣ Eliminar contenedores detenidos
echo "🗑️ Eliminando contenedores muertos..."
docker container prune -f

# 3️⃣ Eliminar imágenes dangling
echo "🧽 Eliminando imágenes dangling..."
dangling=$(docker images -f "dangling=true" -q)
if [[ -n "$dangling" ]]; then
    docker rmi $dangling || true
else
    echo "No hay imágenes dangling."
fi

# 4️⃣ Eliminar imágenes antiguas del webhook si existen
echo "🧹 Eliminando imágenes antiguas del webhook..."
if docker images | grep -q "fastapi_webhook"; then
    docker rmi fastapi_webhook:latest || true
    echo "Imagen fastapi_webhook eliminada."
else
    echo "No existe imagen antigua fastapi_webhook."
fi

# 5️⃣ Limpieza segura de imágenes no utilizadas
echo "🧽 Limpiando imágenes no utilizadas..."
docker image prune -f

# 6️⃣ Reconstruir imágenes desde cero
echo "🔨 Reconstruyendo contenedores..."
docker compose build --no-cache

# 7️⃣ Levantar servicios
echo "⬆️  Levantando contenedores..."
docker compose up -d

# 8️⃣ Mostrar estado final
echo "🔍 Estado de contenedores:"
docker compose ps

echo "=========================================="
echo "🎉 Actualización completada con éxito"
echo "=========================================="
