import socket
import rfid_library  # Substitua pelo nome correto da biblioteca do seu sensor RFID

# Configurações do servidor
HOST = 'seu_endereco_ip_da_raspberry'  # Substitua pelo IP da Raspberry Pi
PORT = 12345  # Porta para comunicação

# Inicializar o sensor RFID
rfid_sensor = rfid_library.RFID()  # Substitua pelo código correto de inicialização do seu sensor

# Inicializar o servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)  # Pode ajustar o número máximo de conexões pendentes

print("Aguardando conexões de clientes...")

try:
    while True:
        # Aguardar conexão de um cliente
        client_socket, client_address = server_socket.accept()
        print("Conexão estabelecida com", client_address)

        # Ler sinal do cliente
        signal = client_socket.recv(1024).decode()

        if signal == "READ_SENSORS":
            # Ler etiquetas do sensor RFID
            detected_tags = rfid_sensor.read_tags()  # Substitua pelo código correto para ler as etiquetas

            # Enviar dados para o cliente
            data_to_send = ",".join(detected_tags) if detected_tags else "Nenhum dado lido"
            client_socket.send(data_to_send.encode())
            print("Dados enviados:", data_to_send)

        # Encerrar a conexão com o cliente atual
        client_socket.close()

finally:
    # Encerrar conexões e limpar recursos
    server_socket.close()
    rfid_sensor.close()  # Substitua pelo código correto para encerrar o sensor RFID
