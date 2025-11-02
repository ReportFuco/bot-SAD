#!/bin/bash

# Script para automatizar la actualización de contenedores Docker Compose
# Autor: Francisco (automatización full 😎)
# Uso: chmod +x update_docker.sh && ./update_docker.sh

# 🚨 Salir si ocurre un error
set -e

# 📍 Ir al directorio donde está el docker-compose.yml
cd "$(dirname "$0")"

# 🕒 Mostrar fecha y hora
echo "=========================================="
echo "  🚀 Actualización de contenedores Docker"
echo "  Fecha: $(date)"
echo "=========================================="

# 📦 Apagar contenedores antiguos
echo "🛑 Deteniendo contenedores..."
docker compose down

# 🧹 Limpiar imágenes antiguas sin uso
echo "🧽 Limpiando imágenes no utilizadas..."
docker image prune -f

# 🔧 Reconstruir imágenes
echo "🔨 Reconstruyendo contenedores..."
docker compose build --no-cache

# 🆙 Levantar en segundo plano
echo "⬆️  Levantando contenedores..."
docker compose up -d

# ✅ Verificar estado
echo "🔍 Estado de los contenedores:"
docker compose ps

echo "=========================================="
echo "🎉 Actualización completada con éxito"
echo "=========================================="
