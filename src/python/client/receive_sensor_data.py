import socket
import ast
from helpers import file

# Configurações do cliente
HOST = file.env("RASPBERRY_IP")  #IP da Raspberry PI
PORT = int(file.env("RASPBERRY_SOCKET_PORT"))  # Porta para comunicação

def receive_data():
    # Inicializar o cliente
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    data_received = None
    print("Conexão estabelecida com a Raspberry Pi")

    data_to_send = "READ_SENSORS"
    try:
        sent_bytes = client_socket.send(data_to_send.encode())
        if sent_bytes == len(data_to_send):
            # Receber dados da Raspberry Pi
            data_received = client_socket.recv(1024).decode()
            data_received = data_received.split(',') if data_received else None
    except Exception as e:
        print(e)
    finally:
        # Encerrar a conexão
        client_socket.close()
        return data_received