from shop_admin import configure_raspberry
from helpers import menu
from helpers import input as ipt
from helpers import file
from helpers import dict
from helpers import sensor
from helpers import request as r
import time
from pynput import keyboard

HEADERS = {
    'admin-token': file.env("ADMIN_TOKEN"),
    'accept': 'application/json',
    'content': 'application/json',
    'client-mac-address': r.get_mac_address()
}

PURCHASE_MAJOR_KEYS = [
    "id", "created_at", "total_value", "status",
    "origin_cashier", "purchaser_name", "purchaser_cpf",
    "payment_method"
]

STOP_RASPBERRY_SERVER_COMMAND = "STOP_SERVER"

stop_purchases_watch = False

def prepare_system():
    configure_raspberry.deploy_raspberry_server()
    success = True
    j = 4
    for i in range(2, -1, -1):
        while (j >= 1):
            print(f"Testando estado da conexão, por favor, aguarde {4 * i + j} segundo(s) a partir de agora...")
            time.sleep(1)
            j -= 1
        success = sensor.sent_message('TESTING')
        if not success:
            print('Falha ao ativar o sensor!')
            return False
        j = 4
    print('Leitor ativado com sucesso!')
    return True

def show_cashiers_info():
    response = r.get('cashiers', HEADERS)
    r.render_response_message(response)
    if r.is_success(response):
        menu.render_cashiers(response.json().get('data'))

def block_cashiers():
    cashier_id = input("Informe o ID do caixa que pretende bloquear: ")
    response = r.post(f"cashiers/{cashier_id}/manage", HEADERS, {'status' : 'block'})
    r.render_response_message(response)

def unblock_cashiers():
    cashier_id = input("Informe o ID do caixa que pretende desbloquear: ")
    response = r.post(f"cashiers/{cashier_id}/manage", HEADERS, {'status' : 'release'})
    r.render_response_message(response)

def show_purchases_history():
    response = r.get("purchases/history", HEADERS)
    r.render_response_message(response)
    if (r.is_success(response)):
        menu.render_purchases(response.json().get('data', []))

def stop_watch_purchases_press_key(pressed_key):
    global stop_purchases_watch
    try:
        if pressed_key.char.lower() == 'n':
            stop_purchases_watch = True
    except AttributeError:
        pass

def track_purchases():
    global stop_purchases_watch
    keyboard_listener = keyboard.Listener(on_press=stop_watch_purchases_press_key)
    print("\nO processo de monitoramento de compras será iniciado a seguir. Para interrompê-lo, pressione 'N' durante 2 segundos assim que o processo iniciar.\n\n")
    dialog_response = ''
    while dialog_response.upper() != 'Y':
        dialog_response = input("Insira 'Y' para confirmar que as instruções foram lidas corretamente e para dar início ao monitoramento: ")
    showed_purchases = {}
    keyboard_listener.start()
    while (not stop_purchases_watch):
        response = r.get("purchases/history", HEADERS, {}, {'order' : 'asc'}).json()
        purchases = response.get("data")
        for i in purchases:
            purchase = purchases[i]
            can_show = True
            if i in showed_purchases:
                modified_values = dict.compare_dicts(showed_purchases[i], purchase, PURCHASE_MAJOR_KEYS)
                can_show = len(modified_values) != 0
                for key, values in modified_values.items():
                    print(f"Compra #{purchase['id']}: A propriedade '{key}' foi modificada de '{values[0]}' para '{values[1]}'")
            if can_show:
                menu.render_purchase(purchase)
            showed_purchases[i] = purchase
        time.sleep(2)
    keyboard_listener.stop()
    stop_purchases_watch = False
        
def register_product():
    bar_codes = sensor.receive_data()
    products = []
    if bar_codes is None:
        print("Nenhum produto foi escaneado!")
    else:
        print("Códigos de barra escaneados: ", bar_codes)
        if input("Para prosseguir com o processo de cadastro de produtos insira 'Y': ").upper() == 'Y':
            for bar_code in bar_codes:
                product = {}
                print(f"Cadastro de informações para o código de barras #{bar_code}")
                product['name'] = input('\tInsira o nome do produto: ')
                product['price'] = ipt.input_number('\tInsira o preço do produto: ')
                product['stock_quantity'] = ipt.input_integer('\tInsira a quantidade em estoque: ')
                product['bar_code'] = bar_code
                products.append(product)
            response = r.post('products/new', HEADERS, {'products': products})
            r.render_response_message(response)
            if r.is_success(response):
                menu.render_products(response.json().get('data'))
        else:
            print('Cadastro de produtos cancelado!')

def edit_product_details():
    details = {}
    id = input("Informe o ID do produto que deseja alterar: ")
    if input("Insira 'Y' para alterar o estoque: ").upper() == 'Y':
        details['stock_quantity'] = ipt.input_integer('Nova quantidade em estoque: ')
    if input("Insira 'Y' para alterar o nome: ").upper() == 'Y':
        details['name'] = input("Novo nome: ")
    if input("Insira 'Y' para alterar preço: ").upper() == 'Y':
        details['price'] = ipt.input_number('Novo preço: ')
    if details:
        response = r.post(f"products/{id}/edit", HEADERS, details)
        r.render_response_message(response)
    else:
        print("Nenhuma alteração definida. Cancelando operação...")

def list_products():
    response = r.get('products', HEADERS)
    r.render_response_message(response)
    if r.is_success(response):
        menu.render_products(response.json().get('data'))

def disable_sensor():
    if input("Tem certeza que deseja desativar o sensor de leitura de produtos? Fazendo isso, os caixas estarão inoperantes! Insira 'Y' para confirmar ou qualquer outro valor para cancelar o procedimento: ").upper() == 'Y':
        if sensor.sent_message(STOP_RASPBERRY_SERVER_COMMAND):
            print("Sensor desativado com sucesso!")
            return True
        print("Falha ao desativar o sensor remotamente! Será necessário desativa-lo manualmente.")
        return False
    print("O procedimento de desativação do sensor de leitura foi cancelado!")
    return False

# def track_cashiers():
#     showed