import requests;
from shop_admin import configure_raspberry
from helpers import file
from helpers import menu

BASE_URL = file.env("API_URL")

def headers():
    return {
        'admin-token': file.env("ADMIN_TOKEN"),
        'accept': 'application/json',
        'content': 'application/json'
    }

def is_success(response):
    return response.status_code >= 100 or response.status_code < 400

def get(endpoint, body = {}, query = {}):
    return requests.get(BASE_URL + "/" + endpoint, data = body, params = query, headers = headers())

def post(endpoint, body = {}, query = {}):
    return requests.get(BASE_URL + "/" + endpoint, data = body, params = query, headers = headers())

def prepare_system():
    try:
        configure_raspberry.deploy_raspberry_server()
        print('Preparando sistema...')
    except Exception as e:
        print("Erro:", e)

def show_cashiers_info():
    response = get('cashiers')
    if (is_success(response)):
        cashiers = response.json()['data']
        for i in cashiers:
            cashier = cashiers[i]
            print(f"Exibindo informações para o caixa {cashier['id']}:")
            print(f"\tID: {cashier['id']}")
            print(f"\tIP: {cashier['ip']}")
            print(f"\tBloqueado: {'Sim' if cashier['is_blocked'] else 'Não'}")
            print(f"\tQuantidade de compras registradas: {len(cashier['registered_purchases'])}")
            menu.scroll_console(2)
    else:
        print(response.json()['message'])

def block_cashiers():
    cashier_id = input("Informe o ID do caixa que pretende bloquear: ")
    response = post(f"cashiers/{cashier_id}/manage", {'status' : 'block'})
    if (is_success(response)):
        print(response.json()['message'])
    else:
        print(response.json()['message'])

def unblock_cashiers():
    cashier_id = input("Informe o ID do caixa que pretende desbloquear: ")
    response = post(f"cashiers/{cashier_id}/manage", {'status' : 'release'})
    if (is_success(response)):
        print(response.json()['message'])
    else:
        print(response.json()['message'])

def show_purchases_history():
    response = get("purchases/history")
    

def track_purchases():
    return