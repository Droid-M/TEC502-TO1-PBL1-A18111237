# Use a imagem base fullaxx/ubuntu-desktop
FROM fullaxx/ubuntu-desktop

# Autor do Dockerfile (opcional)
LABEL maintainer="Marcos Vinícius (droid-M)"

# Atualize os pacotes
RUN apt-get update

# Instale o pacote 'kbd' para resolver o erro "No such file or directory: 'dumpkeys'"
RUN apt-get install -y kbd

# Instale o Python 3
RUN apt-get install -y python3

# Instale o pip para Python 3
RUN apt-get install -y python3-pip

# Instale as dependências de desenvolvimento
RUN apt-get install -y libffi-dev libssl-dev libx11-dev locales

# Limpe o cache de pacotes e diretórios temporários
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Defina o diretório de trabalho no container
WORKDIR /app

# Copie os arquivos de código-fonte para o diretório de trabalho
COPY src/ /app

# Instale as bibliotecas Python a partir do arquivo requirements.txt
RUN pip install -r /app/requirements.txt

# Configura a variável de ambiente para usar o português do Brasil
ENV LANG pt_BR.UTF-8
ENV LC_ALL pt_BR.UTF-8

# Configura a variável de ambiente DISPLAY
ENV DISPLAY=:0
ENV XAUTHORITY=/root/.Xauthority

# Comando para executar o script principal (cashier_menu.py)
CMD ["python3", "python/client/cashier_menu.py"]
