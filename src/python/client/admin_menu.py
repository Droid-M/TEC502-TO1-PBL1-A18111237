from helpers import menu
from helpers import file
from shop_admin import menu as shop_admin_menu
from shop_admin import ssh_open_connection as ssh
from getpass import getpass

def auth():
    key = getpass("Insira a chave de administrador para ter acesso ao sistema: ")
    while key != file.env('ADMIN_TOKEN'):
        key = getpass('Chave incorreta! Insira a chave de administrador para ter acesso ao sistema: ')

def main():
    ssh.init_connection()

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
            print("4 - Reiniciar")

            option = input("Digite o número da opção desejada: ")

            if option == '1':
                menu.scroll_console()
                shop_admin_menu.main(data)
            elif option == '2':
                can_scroll_console = False
                menu.clear_console()
            elif option == '3':
                ssh.close_connection()
                menu.close()
            elif option == '4':
                ssh.close_connection()
                menu.restart()
            else:
                print("Opção inválida. Por favor, escolha uma opção válida.")
            
            can_scroll_console = True
        except Exception as e:
            # raise e
            print(f'Ops! Algo errado aconteceu: "{e}"')
            print("\n-----Recomendamos fortemente que reinicie a aplicação.\n\n")

if __name__ == "__main__":
    auth()
    main()

