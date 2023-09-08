from shop_admin import configure_raspberry
from helpers import menu
from helpers import file
from helpers import dict
from helpers import request as r
import keyboard
import time

HEADERS = {
    'admin-token': file.env("ADMIN_TOKEN"),
    'accept': 'application/json',
    'content': 'application/json'
}

PURCHASE_MAJOR_KEYS = [
    "id", "created_at", "total_value", "status",
    "origin_cashier", "purchaser_name", "purchaser_cpf",
    "payment_method"
]

def prepare_system():
    configure_raspberry.deploy_raspberry_server()
    print('Preparando sistema...')

def show_cashiers_info():
    response = r.get('cashiers', HEADERS)
    r.render_response_message(response)
    if (r.is_success(response)):
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

def track_purchases():
    showed_purchases = {}
    print("\nO processo de monitoramento de compras será iniciado a seguir. Para interrompê-lo, pressione 'N' durante 2 segundos assim que o processo iniciar.\n\n")
    dialog_response = ''
    while dialog_response.upper() != 'Y':
        dialog_response = input("Pressione 'Y' para confirmar que as instruções foram lidas corretamente e para dar início ao monitoramento: ")
    
    while (not keyboard.is_pressed('N')) and not keyboard.is_pressed('n'):
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
        
def register_product():
    return

def edit_product_stock();
    return