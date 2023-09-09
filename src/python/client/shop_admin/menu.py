from helpers import menu
from shop_admin import manager

def main(data):
    cancelMenu = False
    while not cancelMenu:
        menu.scroll_console()
        print("Menu do administrador:")
        print("0 - Retornar")
        if not data['enabled_cashier']:
            print("1 - Ativar leitor de produtos")
        else:
            print("2 - Desativar leitor de produtos")
        print("3 - Consultar informações sobre caixas")
        print("4 - Bloquear caixa")
        print("5 - Liberar caixa")
        print("6 - Consultar histórico de compras")
        print("7 - Acompanhar compras")
        print("8 - Consultar informações sobre produtos registrados")
        if data['enabled_cashier']:
            print("9 - Registrar produtos")
        print("10 - Editar produto")

        option = input("Digite o número da opção desejada: ")

        if option == '0':
            cancelMenu = True
        else:
            if not data['enabled_cashier']:
                if option == '1':
                    manager.prepare_system()
                    data['enabled_cashier'] = True
                    menu.pause()
                    continue
            else:
                if option == '2':
                    data['enabled_cashier'] = not manager.disable_sensor()
                    menu.pause()
                    continue
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
            elif option == '8':
                manager.list_products()
                menu.pause()
            elif option == '9' and data['enabled_cashier']:
                manager.register_product()
                menu.pause()
            elif option == '10':
                manager.edit_product_details()
                menu.pause()
            else:
                    print("Opção inválida. Por favor, escolha uma opção válida.")