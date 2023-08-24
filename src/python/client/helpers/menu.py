import os

def sair():
    print("Saindo do programa.")
    exit()

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def scroll_console():
    for _ in range(10):
        print()