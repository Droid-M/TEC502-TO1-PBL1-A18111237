from helpers import file
from shop_admin import ssh_open_connection as ssh
import time

# Caminho remoto na Raspberry Pi onde o script será copiado
remote_script_path = file.env("RASPBERRY_WORK_DIRECTORY") + "server.py"

ssh.init_connection()

# Executando remotamente o comando para executar o script do servidor na Raspberry Pi
channel = ssh.ssh_client.get_transport().open_session()

# Aguardar até que o comando seja concluído
stdin, stdout, stderr = ssh.ssh_client.exec_command(f'python3 {remote_script_path}')
print(stdout.read().decode('utf-8'))
print(stderr.read().decode('utf-8'))
for line in iter(stdout.readline, ""):
    print(line, end="")
# channel.recv_exit_status()
ssh.close_connection()