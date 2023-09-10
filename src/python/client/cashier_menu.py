from helpers import menu
from helpers import file
from cashier import menu as cashier_menu
from getpass import getpass
from cashier import manager
from requests import exceptions

def auth():
    key = getpass("Insira a chave de caixista para ter acesso ao sistema: ")
    while key != file.env('CASHIER_TOKEN'):
        key = getpass('Chave incorreta! Insira a chave de caixista para ter acesso ao sistema: ')

def main():
    data = {
        'cashier_locked' : False,
        'checkout_status' : None,
        'bar_codes' : None,
        'purchase' : None,
        'cashier_is_registered': None
    }
    can_scroll_console = False

    while True:
        try:
            if can_scroll_console:
                menu.scroll_console()
            print("Menu:")
            print("1 - Caixa")
            print("2 - Limpar console")
            print("3 - Sair")
            print("4 - Reiniciar")

            option = input("Digite o número da opção desejada: ")

            if option == '1':
                if data['cashier_is_registered'] == None:
                    manager.register_cashier_me()
                    data['cashier_is_registered'] = True
                menu.scroll_console()
                cashier_menu.main(data)
            elif option == '2':
                can_scroll_console = False
                menu.clear_console()
            elif option == '3':
                menu.close()
            elif option == '4':
                menu.restart()
            else:
                print("Opção inválida. Por favor, escolha uma opção válida.")
            
            can_scroll_console = True
        except exceptions.ConnectionError:
            print("Ops! Aconteceu um problema na comunicação com o servidor. Por favor, verifique sua conexão com a internet e tente novamente...")
        except Exception as e:
            # raise e
            print(f'Ops! Algo errado aconteceu: "{e}"')
            print("\n-----Recomendamos fortemente que reinicie a aplicação...\n\n")
            # if input("Insira 'Y' para permitir o reinicio da aplicação ou insira qualquer outro valor para prosseguir com o fluxo atual: ").upper() == 'Y':
            #     menu.restart()

if __name__ == "__main__":
    auth()
    main()
