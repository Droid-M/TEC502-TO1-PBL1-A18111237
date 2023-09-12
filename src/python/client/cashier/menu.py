from helpers import menu
from cashier import manager
# import asyncio

# async def check_status(data):
#     data['cashier_locked'] = manager.check_cashier_block_status()

def check_status(data):
    """Informa a situação do caixa"""
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
            print('2 - Registrar e validar compra')
        elif data['checkout_status'] == 'SCANNED_PRODUCTS':
            print('3 - Pagar compra')
            print('4 - Cancelar compra')
        print('5 - Verificar a situação do caixa')

        option = input("Digite o número da opção desejada: ")

        if option == '0':
            cancel_menu = True
        # Se a opção escolhida for a de leitura de etiquetas e não houver nenhuma compra em processo de pagamento, então permita que produtos sejam escaneados (ou re-escaneados):
        elif option == '1' and (data['checkout_status'] == None or data['checkout_status'] == 'SCANNING_PRODUCTS'):
            if not data['cashier_locked']: # Se o caixa não estiver bloqueado, leia as etiquetas dos produtos:
                data['bar_codes'] = manager.scan_products()
                if data['bar_codes'] is None: #Se nenhuma etiqueta for lida, informe ao usuário:
                    print('Nenhum produto foi escaneado!')
                else:
                    print('Códigos de barra escaneados: ', data['bar_codes'])
                    data['checkout_status'] = 'SCANNING_PRODUCTS' # Indica que o processo de leitura de etiquetas foi efetuado com sucesso
            else:
                print("Operação não permitida pois o caixa está bloqueado!")
            menu.pause()
        # Se a opção escolhida for a de registro de compra e o processo de leitura de etiquetas foi efetuado, faça:
        elif option == '2' and data['checkout_status'] == 'SCANNING_PRODUCTS':
            if isinstance(data['bar_codes'], list) and len(data['bar_codes']) > 0: #Se houver ao menos uma etiqueta lida, então prossiga:
                data['purchase'] = manager.register_purchase(data['bar_codes'])
                if isinstance(data['purchase'], dict) and len(data['purchase']) > 0: #Se a copra foi registrada com sucesso no sistema, faça:
                    # Indica que o registro foi um sucesso
                    data['checkout_status'] = 'SCANNED_PRODUCTS'
                else:
                    print("Não foi possível prosseguir com a compra!")
            else:
                print("Houve um problema com os dados escaneados! Por favor, refaça a leitura.")
                # data['checkout_status'] = None
            menu.pause()
        # Se a opção escolhida for '3' ou '4' e o processo de registro foi efetuado com sucesso, faça:
        elif (option == '3' or option == '4') and data['checkout_status'] == 'SCANNED_PRODUCTS':
            if isinstance(data['purchase'], dict) and len(data['purchase']) > 0: #Se os dados da última compra registrada estiverem salvos, faça:
                if option == '3': # Se a opção escolhida foi a de pagamento, faça:
                    if manager.pay_purchase(data['purchase'].get('id')): # Se o pagamento foi efetuado com sucesso, faça:
                        # Limpa da memória as etiquetas lidas, a compra registrada e o status da compra
                        data['bar_codes'] = None
                        data['purchase'] = None
                        data['checkout_status'] = None
                else: #Se a opção escolhida for cancelamento de compra, faça:
                    if manager.cancel_purchase(data['purchase'].get('id')): #Se o cancelamento for efetuado com sucesso, faça:
                        # Limpa da memória as etiquetas lidas, a compra registrada e o status da compra
                        data['bar_codes'] = None
                        data['purchase'] = None
                        data['checkout_status'] = None
            else:
                print("Houve um problema com os dados da compra! Por favor, valide novamente a compra!")
                data['checkout_status'] = 'SCANNING_PRODUCTS' #Indica que o cancelamento ou pagamento da compra falhou
            menu.pause()
        elif option == '5': #Se a opção escolhida for a de consulta de situação do caixa, faça:
            manager.check_cashier_situation() #Consulta e exibe informações sobre o caixa e a ultima compra registrada no servidor (API)
            menu.pause()
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
        