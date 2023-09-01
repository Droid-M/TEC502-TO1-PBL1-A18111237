from pathlib import Path

def env(key):
    with open(Path(__file__).parent.parent.parent.__str__() + "\\.env", "r") as env_file:
        env_vars = env_file.readlines()

    # Percorre as variáveis de ambiente e procura pela variável "ENV"
    for env_var in env_vars:
        if env_var.startswith(f'{key}='):
            return env_var.split("=")[1].strip().strip('"')
    return ''