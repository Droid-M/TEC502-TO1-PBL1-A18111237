from helpers import file
from shop_admin import ssh_open_connection as ssh
import time

# Caminho remoto na Raspberry Pi onde o script será copiado
remote_script_path = file.env("RASPBERRY_WORK_DIRECTORY") + "server.py"

ssh.init_connection()

# Executa remotamente o comando para executar o script do servidor na Raspberry Pi
channel = ssh.ssh_client.get_transport().open_session()
print("Não feche este terminal durante o uso da sua aplicação!")
stdin, stdout, stderr = ssh.ssh_client.exec_command(f'python3 {remote_script_path}')
for line in iter(stdout.readline, ""):
    print(line, end="")

# Aguarda até que o comando seja concluído
channel.recv_exit_status()
ssh.close_connection()