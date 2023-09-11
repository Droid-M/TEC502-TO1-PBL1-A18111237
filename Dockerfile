# # Use a imagem base Python 3.11
# FROM python:3.11

# Use a imagem oficial do Debian slim como base
FROM debian:bullseye-slim

# Atualize os pacotes e instale as dependências necessárias, incluindo o Python 3
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip libffi-dev libssl-dev libx11-dev locales && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir /app

# Defina o diretório de trabalho no container
WORKDIR /app

# Copie os arquivos de código-fonte para o diretório de trabalho
COPY src/ /app

# Instale as bibliotecas Python a partir do arquivo requirements.txt
RUN pip install -r requirements.txt

RUN sed -i '/pt_BR.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen

# Configura a variável de ambiente para usar o português do Brasil
ENV LANG pt_BR.UTF-8
ENV LC_ALL pt_BR.UTF-8
# Configura a variável de ambiente DISPLAY
ENV DISPLAY=:0

ENV XAUTHORITY=/root/.Xauthority


# Comando para executar o script principal (admin_menu.py)
CMD ["python3", "python/client/admin_menu.py"]
