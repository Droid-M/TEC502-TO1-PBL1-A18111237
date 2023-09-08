import socket
import os

def env(key):
    with open("server.env", "r") as env_file:
        env_vars = env_file.readlines()

    # Percorre as variáveis de ambiente e procura pela variável "ENV"
    for env_var in env_vars:
        if env_var.startswith(f'{key}='):
            return env_var.split("=")[1].strip().strip('"')
    return ''

# Configurações do servidor
HOST = env("RASPBERRY_IP")  # Substitua pelo IP da Raspberry Pi
PORT = int(env("RASPBERRY_SOCKET_PORT"))  # Porta para comunicação

# Inicializar o servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)  # Pode ajustar o número máximo de conexões pendentes
signal = None

print("Aguardando conexões de clientes...")

try:
    while not os.path.exists("close_raspberry_server.txt") and signal != "STOP_SERVER":
        # Aguardar conexão de um cliente
        client_socket, client_address = server_socket.accept()
        print("Conexão estabelecida com", client_address)

        # Ler sinal do cliente
        signal = client_socket.recv(1024).decode()

        print(signal)

        if signal == "READ_SENSORS":
            # Enviar dados para o cliente
            data_to_send = "[b'E2002047381502180820C296', b'0000000000000000C0002403']"
            client_socket.send(data_to_send.encode())
            print("Dados enviados:", data_to_send)

        # Encerrar a conexão com o cliente atual
        client_socket.close()

finally:
    # Encerrar conexões e limpar recursos
    server_socket.close()
