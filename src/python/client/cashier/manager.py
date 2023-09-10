from helpers import menu
from helpers import input as ipt
from helpers import file
from helpers import dict
from helpers import sensor
from helpers import request as r

HEADERS = {
    'cashier-token': file.env('CASHIER_TOKEN'),
    'accept': 'application/json',
    'content': 'application/json',
    'client-mac-address': r.get_mac_address()
}

SORTED_PAYMENT_METHODS = {
    1 : 'credit_card',
    2 : 'pix',
    3 : 'cash'
}

def register_cashier_me():
    print('Registrando caixa no sistema...')
    response = r.post('cashiers/register', HEADERS)
    r.render_response_message(response)

def check_cashier_block_status():
    response = r.get('cashiers/me/blocking-status', HEADERS)
    r.render_response_message(response)
    if r.is_success(response):
        return response.json().get('data')['is_blocked']
    return None

def scan_products():
    return sensor.receive_data()

def register_purchase(bar_codes):
    if input("Para prosseguir com a compra, insira 'Y': ").upper() == 'Y':
        response = r.post('purchases/register', HEADERS, {'products_bar_code' : bar_codes})
        r.render_response_message(response)
        if r.is_success(response):
            print("Compra processada: ")
            purchase = response.json().get('data')
            menu.render_purchase(purchase)
            return purchase
        return None
    else:
        print("Compra cancelada!")
        return None

def pay_purchase(purchase_id):
    purchase = {}
    if input("Para confirmar o pagamento da compra, insira 'Y': ").upper() == 'Y':
        payment_method = ipt.input_integer("Informe a forma de pagamento:\n\t1 - Cartão de crédito\n\t2 - Pix\n\t3 - Dinheiro em espécie\nSua escolha: ")
        while not (payment_method >= 1 and payment_method <= 3):
            print("Opção inválida!")
            payment_method = ipt.input_integer("Informe a forma de pagamento:\n\t1 - Cartão de crédito\n\t2 - Pix\n\t3 - Dinheiro em espécie\nSua escolha: ")
        purchase['payment_method'] = SORTED_PAYMENT_METHODS[int(payment_method)] # type: ignore
        if input("Insira 'Y' se deseja registrar o nome e CPF do cliente na compra: ").upper() == 'Y':
            purchase['purchaser_name'] = input("Informe o nome do cliente: ")
            purchase['purchaser_cpf'] = ipt.input_cpf("Informe o CPF do cliente: ")
        response = r.post(f'purchases/{purchase_id}/pay', HEADERS, purchase)
        r.render_response_message(response)
        if r.is_success(response):
            menu.render_purchase(response.json().get('data'))
            return True
    return False

def cancel_purchase(purchase_id):
    if input("Para confirmar o cancelamento da compra, insira 'Y': ").upper() == 'Y':
        response = r.post(f'purchases/{purchase_id}/cancel', HEADERS)
        r.render_response_message(response)
        return r.is_success(response)
    return False