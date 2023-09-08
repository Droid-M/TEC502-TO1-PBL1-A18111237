from shop_admin import configure_raspberry
from helpers import menu
from helpers import file
from helpers import request as r

HEADERS = {
    'admin-token': file.env("ADMIN_TOKEN"),
    'accept': 'application/json',
    'content': 'application/json'
}

def prepare_system():
    configure_raspberry.deploy_raspberry_server()
    print('Preparando sistema...')

def show_cashiers_info():
    response = r.get('cashiers', HEADERS)
    print(response.json()['message'])
    if (r.is_success(response)):
        cashiers = response.json()['data']
        for i in cashiers:
            menu.render_cashier(cashiers[i])
        if (input("Insira 'Y' para consultar detalhes sobre as compras efetuadas por algum dos caixas ou insira qualquer outro valor para ver as próximas ações: ").upper() == 'Y'):
            id = input("Insira o ID do caixa: ")
            if id in cashiers:
                menu.render_purchases(cashiers[id]['registered_purchases'])
            else:
                print("O ID informado não pertence a nenhum dos caixas listados anteriormente!")
        

def block_cashiers():
    cashier_id = input("Informe o ID do caixa que pretende bloquear: ")
    response = r.post(f"cashiers/{cashier_id}/manage", HEADERS, {'status' : 'block'})
    print(response.json()['message'])

def unblock_cashiers():
    cashier_id = input("Informe o ID do caixa que pretende desbloquear: ")
    response = r.post(f"cashiers/{cashier_id}/manage", HEADERS, {'status' : 'release'})
    print(response.json()['message'])

def show_purchases_history():
    response = r.get("purchases/history", HEADERS)
    print(response.json()['message'])
    if (r.is_success(response)):
        purchases = response.json()['data']
        menu.render_purchases(purchases)
        if (input("Insira 'Y' para consultar detalhes sobre os produtos usados nessa compra ou insira qualquer outro valor para ver as próximas ações: ").upper() == 'Y'):
            id = input("Insira o ID da compra: ")
            if id in purchases:
                menu.render_purchases(purchases[id]['products'])
            else:
                print("O ID informado não pertence a nenhuma das compras listadas anteriormente!")

def track_purchases():
    return