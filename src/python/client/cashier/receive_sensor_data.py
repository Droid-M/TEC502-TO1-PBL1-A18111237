import socket

# Configurações do cliente
HOST = 'seu_endereco_ip_da_raspberry'  # Substitua pelo IP da Raspberry Pi
PORT = 12345  # Porta para comunicação

def receive_data():
    # Inicializar o cliente
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    print("Conexão estabelecida com a Raspberry Pi")

    try:
        # Enviar sinal para a Raspberry Pi ler os sensores
        client_socket.send("READ_SENSORS".encode())
        
        # Receber dados da Raspberry Pi
        data_received = client_socket.recv(1024).decode()
    finally:
        # Encerrar a conexão
        client_socket.close()
        return data_received
