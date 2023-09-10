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
    global selected_env_path
    global env_folder_path
    if selected_env_path is None:
        selected_env_path = env_folder_path + "/" + read_env(env_folder_path + "/.env", 'SELECTED_ENV')
    return read_env(selected_env_path, key)

def get_env_path():
    global selected_env_path
    return selected_env_path