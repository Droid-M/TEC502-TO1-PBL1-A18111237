from helpers import menu
from helpers import file
from cashier import menu as cashier_menu
from getpass import getpass
from cashier import manager
from requests import exceptions
from json import decoder

def auth():
    """Exige uma senha de Caixista para liberar o acesso ao menu/programa"""
    key = getpass("Insira a chave de caixista para ter acesso ao sistema: ")
    while key != file.env('CASHIER_TOKEN'):
        key = getpass('Chave incorreta! Insira a chave de caixista para ter acesso ao sistema: ')

def main():
    data = {
        'cashier_locked' : False, #Indica se o caixa está bloqueado
        'checkout_status' : None, #Indica o status da compra (lendo produtos, validando, pagando, cancelando)
        'bar_codes' : None, #Registra os "códigos dos produtos" lidos na ultima compra
        'purchase' : None, #Registra dados da ultima compra validada
        'cashier_is_registered': None #Indica se o caixa está registrado no sistema (api) do Mercado
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
                if data['cashier_is_registered'] == None: #Na primeira execução do laço 'while', o aplicativo sempre considerará que o caixa não está registrado (por mais que ele esteja)
                    manager.register_cashier_me() #Registra o caixa (ou pelo menos tenta)
                    data['cashier_is_registered'] = True
                menu.scroll_console()
                cashier_menu.main(data) #Acessa o menu do caixa após a tentativa de registro do caixa. Isso implica que qualquer falha ao tentar se registrar impedirá o caixa de acessar o menu de caixista
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
        except decoder.JSONDecodeError:
            print("Ops! Aconteceu um problema na comunicação com o servidor. Por favor, verifique sua conexão com a internet e tente novamente...")
        except ConnectionRefusedError:
            print("Ops! Aconteceu um problema na comunicação com o servidor. Por favor, entre em contato com o administrador e solicite o reinicio do sistema de leitura do sensor.")
        except Exception as e:
            print(f'Ops! Algo errado aconteceu: "{e}"')
            print("\n-----Recomendamos fortemente que reinicie a aplicação.\n\n")

if __name__ == "__main__":
    auth()
    main()
