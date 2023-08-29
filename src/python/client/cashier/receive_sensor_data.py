import socket

# Configurações do cliente
HOST = '172.16.103.0'  #IP da Raspberry PI
PORT = 9000  # Porta para comunicação

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
        print(data_received)
        print(len(data_received))
    finally:
        # Encerrar a conexão
        client_socket.close()
        return data_received

receive_data()