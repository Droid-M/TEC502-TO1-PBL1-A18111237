import requests;
from shop_admin import configure_raspberry
from helpers import file
from helpers import menu

def enable_cashier():
    try:
        configure_raspberry.deploy_raspberry_server();
        print('Habilitando caixas...')
        return True
    except Exception as e:
        print("Erro:", e)
        return False

def headers():
    return {
        'admin-token': file.env("ADMIN_TOKEN"),
        'accept': 'application/json',
        'content': 'application/json'
    }

def is_success(status_code):
    return status_code >= 100 or status_code < 400

def show_cashiers_info():
    response = requests.get(file.env("API_URL") + '/cashiers', headers = headers())
    if (is_success(response.status_code)):
        cashiers = response.json()['data']
        for i in cashiers:
            cashier = cashiers[i]
            print(f"Exibindo informações para o caixa {cashier['id']}:")
            print(f"\tIP: {cashier['ip']}")
            print(f"\tIP: {cashier['ip']}")
            print(f"\tBloqueado: {'Sim' if cashier['is_blocked'] else 'Não'}")
            print(f"\tQuantidade de compras registradas: {len(cashier['registered_purchases'])}")
            menu.scroll_console(2)
    else:
        print("Não foi possível consultar informações sobre caixa!")

def block_cashier():
    return

def show_purchases_history():
    return

def track_purchases():
    return