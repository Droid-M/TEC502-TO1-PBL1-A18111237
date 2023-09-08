from helpers import menu
from shop_admin import manager

def main(data):
    cancelMenu = False
    while not cancelMenu:
        menu.scroll_console()
        print("Menu do administrador:")
        print("1 - Retornar")
        if not data['enabled_cashier']:
            print("2 - Preparar sistema")
        else:
            print("3 - Consultar informações sobre caixas")
            print("4 - Bloquear caixa")
            print("5 - Liberar caixa")
            print("6 - Consultar histórico de compras")
            print("7 - Acompanhar compras")

        option = input("Digite o número da opção desejada: ")

        if option == '1':
            cancelMenu = True
        else:
            if not data['enabled_cashier']:
                if option == '2':
                    manager.prepare_system()
                    data['enabled_cashier'] = True
                    menu.pause()
                else:
                    print("Opção inválida. Por favor, escolha uma opção válida.")
            else:
                if option == '3':
                    manager.show_cashiers_info()
                    menu.pause()
                elif option == '4':
                    manager.block_cashiers()
                    menu.pause()
                elif option == '5':
                    manager.unblock_cashiers()
                    menu.pause()
                elif option == '6':
                    manager.show_purchases_history()
                    menu.pause()
                elif option == '7':
                    manager.track_purchases()
                    menu.pause()
                else:
                    print("Opção inválida. Por favor, escolha uma opção válida.")