import socket
import mercury
import os
import random

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
server_socket.listen(35)  # Pode ajustar o número máximo de conexões pendentes

signal = None
environment = env('ENV')

if environment == "SIMULATION" or environment == 'TEST':
    def read_tags():
        # etiquetas = []
        # n = random.randint(1, 10)
        # for _ in range(n):
        #     # Gere etiquetas aleatórias (exemplo)
        #     etiqueta = ''.join(random.choice('0123456789ABCDEF') for _ in range(24))
        #     etiquetas.append(etiqueta)
        # return etiquetas
        etiquetas = ['123456789']
        num_itens = random.randint(0, len(etiquetas))
        # Retorne os primeiros 'num_itens' itens da lista
        return etiquetas[:num_itens]
else:
    # Inicializar o sensor RFID
    sensor = mercury.Reader("tmr:///dev/ttyUSB0")
    sensor.set_region("NA2")
    sensor.set_read_plan([1], "GEN2", read_power=2300)
    def read_tags():
        return list(map(lambda tag: tag.epc.decode('UTF-8'), sensor.read()))


print("Aguardando conexões de clientes...")

try:
    while (not os.path.exists("close_raspberry_server.txt")) and signal != 'STOP_SERVER':
        print("...")
        # Aguardar conexão de um cliente
        client_socket, client_address = server_socket.accept()
        print("Conexão estabelecida com", client_address)

        # Ler sinal do cliente
        signal = client_socket.recv(1024).decode()

        print(signal)

        if signal == "READ_SENSORS":
            # Ler etiquetas do sensor RFID
            detected_tags = read_tags()
            # Enviar dados para o cliente
            data_to_send = ",".join(detected_tags) if detected_tags else ''
            client_socket.send(data_to_send.encode())
            print("Dados enviados:", data_to_send)

        # Encerrar a conexão com o cliente atual
        client_socket.close()

finally:
    # Encerrar conexões e limpar recursos
    server_socket.close()
