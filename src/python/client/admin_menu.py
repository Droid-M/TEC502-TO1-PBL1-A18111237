from helpers import menu
from helpers import file
from shop_admin import menu as shop_admin_menu
from shop_admin import ssh_open_connection as ssh

def main():
    ssh.init_connection();

    data = {
        'enabled_cashier' : False
    }

    can_scroll_console = False
    while True:
        try:
            if can_scroll_console:
                menu.scroll_console()
            print("Menu:")
            print("1 - Administrator")
            print("2 - Limpar console")
            print("3 - Sair")

            option = input("Digite o número da opção desejada: ")

            if option == '1':
                menu.scroll_console()
                shop_admin_menu.main(data)
            elif option == '2':
                can_scroll_console = False
                menu.clear_console()
            elif option == '3':
                menu.sair()
            else:
                print("Opção inválida. Por favor, escolha uma opção válida.")
            
            can_scroll_console = True
        except Exception as e:
            raise e
            print(f'Ops! Algo errado aconteceu: "{e}"')
        finally:
            ssh.close_connection()

if __name__ == "__main__":
    main()
