from helpers import menu
from cashier import menu as cashier_menu

def main():
    can_scroll_console = False
    while True:
        if can_scroll_console:
            menu.scroll_console()
        print("Menu:")
        print("1 - Caixa")
        print("2 - Administrator")
        print("3 - Limpar console")
        print("4 - Sair")

        option = input("Digite o número da opção desejada: ")

        if option == '1':
            cashier_menu()
        elif option == '2':
            cashier_menu.main()
        elif option == '3':
            can_scroll_console = False
            menu.clear_console()
        elif option == '4':
            menu.sair()
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
        
        can_scroll_console = True

if __name__ == "__main__":
    main()
