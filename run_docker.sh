#!/bin/bash

# Nome e tag da imagem Docker
IMAGE_NAME="supermarket"
IMAGE_TAG="1.0"

# Verifica se o Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "Docker não está instalado. Por favor, instale o Docker para continuar."
    exit 1
fi

# Constrói a imagem Docker
docker build -t "${IMAGE_NAME}:${IMAGE_TAG}" .

# Verifica se a construção foi bem-sucedida
if [ $? -eq 0 ]; then
    echo "Imagem Docker construída com sucesso: ${IMAGE_NAME}:${IMAGE_TAG}"

    # Executa o contêiner a partir da imagem
    docker run --privileged -it -v /dev/input:/dev/input "${IMAGE_NAME}:${IMAGE_TAG}"
else
    echo "Erro ao construir a imagem Docker."
    exit 1
fi
