import socket
import mercury
import os
import random
from pathlib import Path
import threading

def env(key: str):
    """Vasculha o arquivo de ambientação ('.env') à procura de alguma chave que corresponda à informada e retorna o valor atribuído a essa chave 
    Args: 
        key: Chave cujo valor atribuído no arquivo de ambientação deve ser obtido
    """
    # Copia o conteúdo do arquivo de ambientação para a memória
    with open(Path(__file__).parent.__str__() + "/server.env", "r") as env_file:
        env_vars = env_file.readlines()

    # Percorre as variáveis de ambiente e procura pela variável "ENV"
    for env_var in env_vars:
        if env_var.startswith(f'{key}='):
            return env_var.split("=")[1].strip().strip('"')
    return ''

environment = env('ENV')

if environment == "SIMULATION" or environment == 'TEST':
    def read_tags(): # type: ignore
        """Função com o fim facilitar a execução de testes locais.
        """

        #Para cadastrar produtos:
        # etiquetas = []
        # n = random.randint(1, 2)
        # for _ in range(n):
        #     # Gere etiquetas aleatórias (exemplo)
        #     etiqueta = ''.join(random.choice('0123456789ABCDEF') for _ in range(24))
        #     etiquetas.append(etiqueta)
        # return etiquetas

        #Para criar novas compras:
        etiquetas = ['123456789', 'cc', 'xnxo2lc2023c', 'natjepl10', 'D45014980412A22092F9D569', 'C2B45512AB12DAE9DE3D1922', 'D05E9CDB9F8729563AB5E580', '7F3C670A50F2525AD957EFFF', '66B31F3E924BB07723E579FA']
        num_itens = random.randint(0, len(etiquetas))
        return etiquetas[:num_itens]
else:
    # Inicializar o sensor RFID
    sensor = mercury.Reader("tmr:///dev/ttyUSB0")
    sensor.set_region("NA2")
    sensor.set_read_plan([1], "GEN2", read_power=2300)
    def read_tags():
        """Lê as tags RFID através do sensor (como um conjunto binário), converte de binário para string e as retorna como uma lista de strings"""
        return list(map(lambda tag: tag.epc.decode('UTF-8'), sensor.read()))

def handle_client(client_socket):
    """Recebe e trata a mensagem enviada pelo cliente. Por enquanto, apenas 2 tipos de tratamento são aplicados: Informar as etiquetas lidas; Parar o servidor
    """
    global signal
    try:
        # Lê sinal do cliente
        cli_signal = client_socket.recv(1024).decode()
        print('Mensagem recebida: ', cli_signal)
        if cli_signal == "READ_SENSORS":
            print("Lendo etiquetas através do sensor...")
            # Lê etiquetas do sensor RFID
            detected_tags = read_tags()
            # Envia dados para o cliente
            data_to_send = ",".join(detected_tags) if detected_tags else ''
            client_socket.send(data_to_send.encode())
            print("Dados enviados:", data_to_send)
        elif cli_signal == 'STOP_SERVER':
            print("Registrando o comando de parada...")
            signal = 'STOP_SERVER'
    finally:
        # Encerra a conexão com o cliente atual
        client_socket.close()

def main():
    global signal
    global server_socket
    print("Aguardando conexões de clientes...")
    try:
        # Enquanto não houver um arquivo de texto com o nome sugestivo e nem houver clientes enviando o sinal de parada, faça: 
        while (not os.path.exists("close_raspberry_server.txt")) and signal != 'STOP_SERVER':
            print("...")
            # Aguarda conexão de algum cliente
            client_socket, client_address = server_socket.accept()
            print("Conexão estabelecida com", client_address)

            # Inicia uma nova thread para lidar com o cliente (isso impede o servidor de congestionar requisições caso a leitura RFID esteja lenta)
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()
            print(signal)
    except KeyboardInterrupt:
        print("Servidor encerrado pelo usuário.")
    finally:
        # Encerra conexões e limpar recursos
        print("Servidor encerrado...")
        server_socket.close()
        signal = None

if __name__ == '__main__':
    # Configura o servidor
    HOST = env("RASPBERRY_IP")  # IP da Raspberry Pi
    PORT = int(env("RASPBERRY_SOCKET_PORT"))  # Porta para comunicação

    # Inicializa o servidor
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(35) # (Essa configuração não impede o timeout do cliente, visto que as conexões pendentes ainda não foram aceitas. 
    #Apenas impede as primeiras conexões 34 conexões pendentes de serem recusadas automaticamente) ""

    signal = None

    main()