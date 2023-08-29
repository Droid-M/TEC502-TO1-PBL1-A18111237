from helpers import menu
from cashier import menu as cashier_menu
from shop_admin import menu as shop_admin_menu

def main():
    data = {
        'enabled_cashier' : False
    }

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
            # menu.scroll_console()
            cashier_menu.main(data)
        elif option == '2':
            menu.scroll_console()
            shop_admin_menu.main(data)
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
