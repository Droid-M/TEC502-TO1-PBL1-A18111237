from helpers import menu

def enable_cashier():
    print('Habilitando caixas...')
    return True

def main():
    canScrollConsole = False
    enabledCashier = False
    cancelMenu = False
    while not cancelMenu:
        if canScrollConsole:
            menu.scroll_console()
        print("Menu:")
        print("1 - voltar")
        if not enabledCashier:
            print("2 - Habilitar caixa")

        option = input("Digite o número da opção desejada: ")

        if option == '1':
            menu.sair()
        elif option == '2' and (not enabledCashier):
            enabledCashier = enable_cashier()
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
        
        canScrollConsole = True

if __name__ == "__main__":
    main()
