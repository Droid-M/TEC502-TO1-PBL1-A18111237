from helpers import menu

def enable_cashier():
    print('Habilitando caixas...')
    return True

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