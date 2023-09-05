from helpers import file
from pathlib import Path
from shop_admin import ssh_open_connection as ssh

# Caminho local do script que será copiado para a Raspberry Pi
local_script_path = path = Path(__file__).parent.parent.parent.__str__() + '\\' + file.env("LOCAL_RASPBERRY_SCRIPT_PATH")

# Caminho remoto na Raspberry Pi onde o script será copiado
remote_script_path = file.env("RASPBERRY_WORK_DIRECTORY") + "server.py"

# Caminho local do arquivo de ambientação (.env)
local_env_path = Path(__file__).parent.parent.parent.__str__() + '\\.env'

# Caminho remoto na Raspberry Pi onde o arquivo de ambientação será copiado
remote_env_path = file.env("RASPBERRY_WORK_DIRECTORY") + "server.env"

if file.env("ENV") != "SIMULATION":
    def deploy_raspberry_server():
        # Copiar o arquivo do script para a Raspberry Pi
        with open(local_script_path, 'rb') as local_file:
            sftp = ssh.ssh_client.open_sftp()
            sftp.putfo(local_file, remote_script_path)
            sftp.close()
        with open(local_env_path, 'rb') as local_file:
            sftp = ssh.ssh_client.open_sftp()
            sftp.putfo(local_file, remote_env_path)
            sftp.close()
        print("Arquivo do script copiado para a Raspberry Pi!")

        # Executando remotamente o comando para executar o script do servidor na Raspberry Pi
        # stdin, stdout, stderr = ssh.ssh_client.exec_command(f'python3 {remote_script_path} &')
        # print("Script do servidor iniciado na Raspberry Pi.")
else:
    def deploy_raspberry_server():
        print("Simulação: Arquivo do script copiado para a Raspberry Pi!")
        print("Simulação: Script do servidor iniciado na Raspberry Pi.")
    