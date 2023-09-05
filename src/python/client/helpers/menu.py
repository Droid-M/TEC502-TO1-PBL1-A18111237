import os

def sair():
    print("Saindo do programa.")
    exit()

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def scroll_console(lines = 10):
    for _ in range(lines):
        print()