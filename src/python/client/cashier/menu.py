from helpers import menu
from cashier import manager
# import asyncio

# async def check_status(data):
#     data['cashier_locked'] = manager.check_cashier_block_status()

def check_status(data):
    print("Consultando situação do caixa...")
    status = manager.check_cashier_block_status()
    data['cashier_locked'] = status if status != None else True

def main(data):
    cancel_menu = False
    option = None
    while not cancel_menu:
        # loop = asyncio.get_event_loop()  # Obtém o loop de eventos assíncronos
        # loop.run_until_complete(check_status(data))  # Executa a função assíncrona
        # loop.close()
        check_status(data)
        menu.scroll_console()
        print(f"SITUAÇÃO DO CAIXA: {'BLOQUEADO' if data['cashier_locked'] else 'LIBERADO'}")
        print("Menu do caixa:")
        print("0 - Retornar")
        if data['checkout_status'] == None:
            print('1 - Escanear produtos para a nova compra')
        elif data['checkout_status'] == 'SCANNING_PRODUCTS':
            print('1 - Re-escanear produtos')
            print('2 - Validar compra')
        elif data['checkout_status'] == 'SCANNED_PRODUCTS':
            print('3 - Pagar compra')
            print('4 - Cancelar compra')
        print('5 - Verificar novamente a situação do bloqueio')

        option = input("Digite o número da opção desejada: ")

        if option == '0':
            cancel_menu = True
        elif option == '1' and (data['checkout_status'] == None or data['checkout_status'] == 'SCANNING_PRODUCTS'):
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
                if isinstance(data['purchase'], dict) and len(data['purchase']) > 0:
                    data['checkout_status'] = 'SCANNED_PRODUCTS'
                else:
                    print("Houve um problema com os dados da compra! Por favor, valide novamente a compra!")
            else:
                print("Houve um problema com os dados escaneados! Por favor, refaça a leitura.")
                # data['checkout_status'] = None
            menu.pause()
        elif (option == '3' or option == '4') and data['checkout_status'] == 'SCANNED_PRODUCTS':
            if isinstance(data['purchase'], dict) and len(data['purchase']) > 0:
                if option == '3':
                    if manager.pay_purchase(data['purchase'].get('id')):
                        data['bar_codes'] = None
                        data['purchase'] = None
                        data['checkout_status'] = None
                    else:
                        print('Falha ao pagar a compra!')
                else:
                    if manager.cancel_purchase(data['purchase'].get('id')):
                        data['bar_codes'] = None
                        data['purchase'] = None
                        data['checkout_status'] = None
                    else:
                        print('Falha ao cancelar a compra!')
            else:
                print("Houve um problema com os dados da compra! Por favor, valide novamente a compra!")
                data['checkout_status'] = 'SCANNING_PRODUCTS'
            menu.pause()
        elif option == '5':
            check_status(data)
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
        