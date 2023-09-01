import socket
import ast
from helpers import file

# Configurações do cliente
HOST = file.env("RASPBERRY_IP")  #IP da Raspberry PI
PORT = int(file.env("RASPBERRY_PORT"))  # Porta para comunicação

def receive_data():
    # Inicializar o cliente
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    data_received = None
    print("Conexão estabelecida com a Raspberry Pi")

    try:
        # Enviar sinal para a Raspberry Pi ler os sensores
        client_socket.send("READ_SENSORS".encode())
        
        # Receber dados da Raspberry Pi
        data_received = client_socket.recv(1024).decode()
        data_received = list(ast.literal_eval(data_received))
    finally:
        # Encerrar a conexão
        client_socket.close()
        return data_received