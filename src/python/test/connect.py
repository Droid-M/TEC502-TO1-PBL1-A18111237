import paramiko

# Configurações da conexão SSH
raspberry_ip = '172.16.103.0'
raspberry_username = 'tec502'
raspberry_password = 'larsid'

# Caminho local do script que será copiado para a Raspberry Pi
local_script_path = '../../server/raspberry_server.py'

# Caminho remoto na Raspberry Pi onde o script será copiado

# Estabelecer conexão SSH com a Raspberry Pi
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

command = 'cd TP01/MarcOs/exemplos/py && python3 read.py'

try:
    ssh_client.connect(raspberry_ip, username=raspberry_username, password=raspberry_password)
    print("Conexão SSH estabelecida com a Raspberry Pi.")

    # Executar o comando remotamente
    stdin, stdout, stderr = ssh_client.exec_command(command)
    print("Script do servidor iniciado na Raspberry Pi.")

    # Exibir saída do comando
    print(stdout.read().decode())
except Exception as e:
    print("Erro:", e)
finally:
    # Fechar conexão SSH
    ssh_client.close()
