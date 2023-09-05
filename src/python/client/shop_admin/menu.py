from helpers import menu
from shop_admin import manager

def main(data):
    cancelMenu = False
    while not cancelMenu:
        menu.scroll_console()
        print("Menu do administrador:")
        print("1 - Retornar")
        if not data['enabled_cashier']:
            print("2 - Habilitar caixa")
        else:
            print("3 - Consultar informações sobre caixas")
            print("4 - Bloquear/Liberar caixa")
            print("5 - Consultar histórico de compras")
            print("6 - Acompanhar compras")

        option = input("Digite o número da opção desejada: ")

        if option == '1':
            cancelMenu = True
        else:
            if not data['enabled_cashier']:
                if option == '2':
                    data['enabled_cashier'] = manager.enable_cashier()
                else:
                    print("Opção inválida. Por favor, escolha uma opção válida.")
            else:
                if option == '3':
                    manager.show_cashiers_info()
                elif option == '4':
                    manager.block_cashier()
                elif option == '5':
                    manager.show_purchases_history()
                elif option == '6':
                    manager.track_purchases()
                else:
                    print("Opção inválida. Por favor, escolha uma opção válida.")
        input("Pressione Enter para continuar...")