from helpers import menu
from shop_admin import configure_cashier

def enable_cashier():
    try:
        configure_cashier.deploy_raspberry_server();
        print('Habilitando caixas...')
        return True
    except Exception as e:
        print("Erro:", e)
        return False

def main(data):
    canScrollConsole = False
    cancelMenu = False
    while not cancelMenu:
        if canScrollConsole:
            menu.scroll_console()
        print("Menu do administrador:")
        print("1 - Retornar")
        if not data['enabled_cashier']:
            print("2 - Habilitar caixa")
        print("3 - Consultar informações sobre caixas")
        print("4 - Bloquear/Liberar caixa")
        print("5 - Consultar histórico de compras")
        print("6 - Acompanhar compras")

        option = input("Digite o número da opção desejada: ")

        if option == '1':
            cancelMenu = True
        elif option == '2' and (not data['enabled_cashier']):
            data['enabled_cashier'] = enable_cashier()
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
        # else 
        
        canScrollConsole = True