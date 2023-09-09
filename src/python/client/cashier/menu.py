from helpers import menu
from python.client.cashier import manager

def main(data):
    cancel_menu = False
    option = None
    while not cancel_menu:
        menu.scroll_console()
        print(f"SITUAÇÃO DO CAIXA: {'BLOQUEADO' if data['cashier_locked'] else 'LIBERADO'}")
        print("Menu do caixa:")
        print("0 - Retornar")
        if data['checkout_status'] == None:
            print('1 - Escanear produtos')
        elif data['checkout_status'] == 'SCANNING_PRODUCTS':
            print('2 - Validar compra')
        elif data['checkout_status'] == 'PAY_PURCHASE':
            print('3 - Pagar compra')

        option = input("Digite o número da opção desejada: ")

        if option == '0':
            cancel_menu = True
        elif option == '1' and data['checkout_status'] == None:
            if not data['cashier_locked']:
                data['bar_codes'] = manager.scan_products()
                if data['bar_codes'] is None:
                    print('Nenhum produto foi escaneado!')
                else:
                    print('Códigos de barra escaneados: ', data['bar_codes'])
                    data['checkout_status'] = 'SCANNING_PRODUCTS'
            else:
                print("Operação não permitida pois o caixa está bloqueado!")
            menu.pause()
        elif option == '2' and data['checkout_status'] == 'SCANNING_PRODUCTS':
            if isinstance(data['bar_codes'], list) and len(data['bar_codes']) > 0:
                data['purchase'] = manager.register_purchase(data['bar_codes'])
                data['checkout_status'] = 'PAY_PURCHASE'
            else:
                print("Houve um problema com os dados escaneados! Por favor, refaça a leitura.")
                data['checkout_status'] = None
            menu.pause()
        elif option == '3' and data['checkout_status'] == 'PAY_PURCHASE':
            if isinstance(data['purchase'], dict) and len(data['purchase']) > 0:
                manager.pay_purchase(data['purchase'].get('id'))
            else:
                print("Houve um problema com os dados da compra! Por favor, valide novamente a compra!")
                data['checkout_status'] = 'SCANNING_PRODUCTS'
            menu.pause()
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
        