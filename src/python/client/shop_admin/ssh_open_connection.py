import paramiko

# Configurações da conexão SSH
raspberry_ip = '172.16.103.0'
raspberry_username = 'tec502'
raspberry_password = 'larsid'

ssh_client = paramiko.SSHClient()

def init_connection():
    # Estabelecer conexão SSH com a Raspberry Pi
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(raspberry_ip, username=raspberry_username, password=raspberry_password)
    print("Conexão SSH estabelecida com a Raspberry Pi.")

def get_ssh_client():
    return ssh_client;

def close_connection():
    ssh_client.close()