from helpers import menu
from pathlib import Path
import ssh_open_connection as ssh

# Caminho local do script que será copiado para a Raspberry Pi
local_script_path = path = Path(__file__).parent.parent.parent.__str__() + '\\server\\raspberry_server.py'

# Caminho remoto na Raspberry Pi onde o script será copiado
remote_script_path = 'TP01/MarcOs/raspberry_server.py'

def deploy_raspberry_server():
    # Copiar o arquivo do script para a Raspberry Pi
    with open(local_script_path, 'rb') as local_file:
        sftp = ssh.ssh_client.open_sftp()
        sftp.putfo(local_file, remote_script_path)
        sftp.close()
    print("Arquivo do script copiado para a Raspberry Pi.")

    # Executando remotamente o comando para executar o script do servidor na Raspberry Pi
    stdin, stdout, stderr = ssh.ssh_client.exec_command(f'python3 {remote_script_path} &')
    print("Script do servidor iniciado na Raspberry Pi.")


def enable_cashier():
    try:
        deploy_raspberry_server();
        print('Habilitando caixas...')
        return True
    except Exception as e:
        print("Erro:", e)
        return False

def main(data):
    canScrollConsole = False
    cancelMenu = False
    while not cancelMenu:
        if canScrollConsole:
            menu.scroll_console()
        print("Menu do administrador:")
        print("1 - voltar")
        if not data['enabled_cashier']:
            print("2 - Habilitar caixa")

        option = input("Digite o número da opção desejada: ")

        if option == '1':
            cancelMenu = True
        elif option == '2' and (not data['enabled_cashier']):
            data['enabled_cashier'] = enable_cashier()
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
        
        canScrollConsole = True