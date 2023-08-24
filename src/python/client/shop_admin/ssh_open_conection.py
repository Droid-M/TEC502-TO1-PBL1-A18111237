import paramiko

# Configurações da conexão SSH
raspberry_ip = 'seu_endereco_ip_da_raspberry'
raspberry_username = 'seu_usuario_da_raspberry'
raspberry_password = 'sua_senha_da_raspberry'

# Caminho local do script que será copiado para a Raspberry Pi
local_script_path = '../../server/raspberry_server.py'

# Caminho remoto na Raspberry Pi onde o script será copiado
remote_script_path = '/caminho/remoto/do/script_raspberry.py'

# Comando para executar o script do servidor na Raspberry Pi
command = f'python {remote_script_path}'

# Estabelecer conexão SSH com a Raspberry Pi
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh_client.connect(raspberry_ip, username=raspberry_username, password=raspberry_password)
    print("Conexão SSH estabelecida com a Raspberry Pi.")

    # Copiar o arquivo do script para a Raspberry Pi
    with open(local_script_path, 'rb') as local_file:
        sftp = ssh_client.open_sftp()
        sftp.putfo(local_file, remote_script_path)
        sftp.close()
    print("Arquivo do script copiado para a Raspberry Pi.")

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
