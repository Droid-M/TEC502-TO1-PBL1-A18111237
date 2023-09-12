from pathlib import Path

selected_env_path = None
env_folder_path = Path(__file__).parent.parent.parent.__str__()

def read_env(env_path, key_to_search):
    with open(env_path, "r") as env_file:
        env_vars = env_file.readlines()

    # Percorre as variáveis de ambiente e procura pela variável "ENV"
    for env_var in env_vars:
        if env_var.startswith(f'{key_to_search}='):
            return env_var.split("=")[1].strip().strip('"')
    return ''

def env(key):
    """Vasculha o arquivo de ambientação ('.env') à procura de alguma chave que corresponda à informada e retorna o valor atribuído a essa chave 
    Args: 
        key: Chave cujo valor atribuído no arquivo de ambientação deve ser obtido
    """
    global selected_env_path
    global env_folder_path
    if selected_env_path is None: # Se nenhum arquivo de ambientação padrão tiver sido escolhido, faça:
        # Registra o arquivo de ambientação padrão com base na chave 'SELECTED_ENV' presente no arquivo '.env'
        selected_env_path = env_folder_path + "/" + read_env(env_folder_path + "/.env", 'SELECTED_ENV')
    # Retorna o valor correspondente à chave procurada no arquivo de ambientação padrão
    return read_env(selected_env_path, key)

def get_env_path():
    """Infora o caminho do arquivo de ambientação padrão"""
    global selected_env_path
    return selected_env_path