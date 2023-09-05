import socket
import mercury
import os

# Configurações do servidor
HOST = '172.16.103.0'  # Substitua pelo IP da Raspberry Pi
PORT = 9000  # Porta para comunicação

# Inicializar o sensor RFID
sensor = mercury.Reader("tmr:///dev/ttyUSB0")
sensor.set_region("NA2")
sensor.set_read_plan([1], "GEN2", read_power=2300)

# Inicializar o servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)  # Pode ajustar o número máximo de conexões pendentes

print("Aguardando conexões de clientes...")

try:
    while not os.path.exists("close_raspberry_server.txt"):
        print("...")
        # Aguardar conexão de um cliente
        client_socket, client_address = server_socket.accept()
        print("Conexão estabelecida com", client_address)

        # Ler sinal do cliente
        signal = client_socket.recv(1024).decode()

        print(signal)

        if signal == "READ_SENSORS":
            # Ler etiquetas do sensor RFID
            detected_tags = list(map(lambda tag: tag.epc.decode('UTF-8'), sensor.read()))
            # Enviar dados para o cliente
            data_to_send = ",".join(detected_tags) if detected_tags else "Nenhum dado lido"
            client_socket.send(data_to_send.encode())
            print("Dados enviados:", data_to_send)

        # Encerrar a conexão com o cliente atual
        client_socket.close()

finally:
    # Encerrar conexões e limpar recursos
    server_socket.close()
