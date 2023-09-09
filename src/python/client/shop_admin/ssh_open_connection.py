import paramiko
from helpers import file

# Configurações da conexão SSH
raspberry_ip = file.env("RASPBERRY_IP")
raspberry_username = file.env("RASPBERRY_USERNAME")
raspberry_password = file.env("RASPBERRY_PASSWORD")

ssh_client = paramiko.SSHClient()

if file.env("ENV") != "SIMULATION":
    def init_connection():
        try:
            print("Tentando estabelecer conexão SHH com a Raspberry")
            # Estabelecer conexão SSH com a Raspberry Pi
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(raspberry_ip, username=raspberry_username, password=raspberry_password)
            print("Conexão SSH estabelecida com a Raspberry Pi.")
        except Exception as e:
            print("Erro: ", e)

    def close_connection():
        ssh_client.close()
        print("Conexão SSH encerrada com sucesso")
else:
    def init_connection():
        print("Simulação: Conexão SSH estabelecida com a Raspberry Pi.")

    def close_connection():
        print("Simulação: Conexão SSH encerrada com sucesso!")

def get_ssh_client():
    return ssh_client