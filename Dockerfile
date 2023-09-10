# Use a imagem base Python 3.11
FROM python:3.11

# Defina o diretório de trabalho no container
WORKDIR /app

# Copie os arquivos de código-fonte para o diretório de trabalho
COPY src /app

# Instale as dependências Python do seu projeto
RUN pip install paramiko requests pytz keyboard pynput

# Exponha a porta, se necessário (depende do seu código)
# EXPOSE 8080

# Comando para executar o script principal (admin_menu.py)
CMD ["python", "src/python/client/admin_menu.py"]
