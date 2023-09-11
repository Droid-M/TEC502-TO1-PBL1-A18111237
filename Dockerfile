# Use a imagem base Python 3.11
FROM python:3.11

# Defina o diretório de trabalho no container
WORKDIR /app

# Copie os arquivos de código-fonte para o diretório de trabalho
COPY /src /app

# Instale as dependências do sistema necessárias para as bibliotecas
RUN apt-get update && apt-get install -y libffi-dev libssl-dev libx11-dev

# Instale as bibliotecas Python a partir do arquivo requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt

# Comando para executar o script principal (admin_menu.py)
CMD ["python", "python/client/admin_menu.py"]
