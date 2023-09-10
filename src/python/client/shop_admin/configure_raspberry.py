from helpers import file
from pathlib import Path
from shop_admin import ssh_open_connection as ssh
import subprocess
import os
import sys

# Caminho local do script que será copiado para a Raspberry Pi
local_script_path = path = Path(__file__).parent.parent.parent.__str__() + '/' + file.env("LOCAL_RASPBERRY_SCRIPT_PATH")

# Caminho remoto na Raspberry Pi onde o script será copiado
remote_script_path = file.env("RASPBERRY_WORK_DIRECTORY") + "server.py"

# Caminho local do arquivo de ambientação (.env)

# Caminho remoto na Raspberry Pi onde o arquivo de ambientação será copiado
remote_env_path = file.env("RASPBERRY_WORK_DIRECTORY") + "server.env"

if file.env("ENV") != "SIMULATION":
    def deploy_raspberry_server():
        ssh.init_connection()
        # Copiar o arquivo do script para a Raspberry Pi
        sftp = ssh.ssh_client.open_sftp()
        with open(local_script_path, 'rb') as local_file:
            sftp.putfo(local_file, remote_script_path)
        with open(file.get_env_path(), 'rb') as local_file: 
            sftp.putfo(local_file, remote_env_path)
        sftp.close()
        ssh.close_connection()
        print("Arquivo do script copiado para a Raspberry Pi!")
        if os.name == 'nt':
            subprocess.Popen(['start', 'python', Path(__file__).parent.parent.__str__() + '/run_raspberry_server.py'], shell = True)
        else:
            terminal = os.popen('ls /usr/bin/*terminal*').read().split()[0]
            subprocess.Popen([terminal + ' -e "python3 ' + Path(__file__).parent.parent.__str__() + '/run_raspberry_server.py"'], shell = True)
            # if sys.platform.startswith('win'):
            #     subprocess.Popen(['x-terminal-emulator', '-e', 'python3', Path(__file__).parent.parent.__str__() + '/run_raspberry_server.py'])
            # elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
            #     subprocess.Popen(['xterm', '-e', 'python3', Path(__file__).parent.parent.__str__() + '/run_raspberry_server.py'])

else:
    def deploy_raspberry_server():
        print("Simulação: Arquivo do script copiado para a Raspberry Pi!")
        print("Simulação: Script do servidor iniciado na Raspberry Pi.")
    