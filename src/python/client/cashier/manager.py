from helpers import menu
from helpers import input as ipt
from helpers import file
from helpers import dict
from helpers import sensor
from helpers import request as r

HEADERS = {
    'cashier-token': file.env('CASHIER_TOKEN'), #Sem o cashier-token, qualquer requisição feita para rotas de caixistas será bloqueada
    'accept': 'application/json',
    'content': 'application/json',
    'client-mac-address': r.get_mac_address() #O MAC da máquina é obrigatório pois é a forma mais fiável de identificar o computador na rede
}

SORTED_PAYMENT_METHODS = {
    1 : 'credit_card',
    2 : 'pix',
    3 : 'cash'
}

def register_cashier_me():
    """Tenta registrar o caixa no sistema (API). Caso o caixa já tenha um cadastro, apenas uma mensagem sobre isso é exibida"""
    print('Registrando caixa no sistema...')
    response = r.post('cashiers/register', HEADERS)
    r.render_response_message(response)

def check_cashier_block_status():
    """Verifica e informa a situação de bloqueio do caixa (se está ou não bloqueado) através de um booleano (True para bloqueado e False para desbloqueado)"""
    response = r.get('cashiers/me/blocking-status', HEADERS)
    r.render_response_message(response)
    if r.is_success(response):
        return response.json().get('data')['is_blocked']
    return None

def scan_products():
    """Lê as "etiquetas dos produtos" que estiverem no sensor"""
    return sensor.receive_data()

def register_purchase(bar_codes):
    """Registra uma compra no sistema
    Returns:
        Returna dados (dict) da compra registrada ou None em caso de falha ou cancelamento do registro
    """
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
    """Registra o pagamento de uma compra
    Returns:
        Returna True em caso de sucesso ou Fase em caso de falha ou cancelamento
    """
    purchase = {}
    if input("Para confirmar o pagamento da compra, insira 'Y': ").upper() == 'Y':
        payment_method = ipt.input_integer("Informe a forma de pagamento:\n\t1 - Cartão de crédito\n\t2 - Pix\n\t3 - Dinheiro em espécie\nSua escolha: ")
        while not (payment_method >= 1 and payment_method <= 3): #Enquanto a forma de pagamento não for Cartão, Pix ou Dinheiro, faça:
            print("Opção inválida!")
            payment_method = ipt.input_integer("Informe a forma de pagamento:\n\t1 - Cartão de crédito\n\t2 - Pix\n\t3 - Dinheiro em espécie\nSua escolha: ")
        purchase['payment_method'] = SORTED_PAYMENT_METHODS[int(payment_method)] # type: ignore
        if input("Insira 'Y' se deseja registrar o nome e CPF do cliente na compra: ").upper() == 'Y':
            # Captura o nome e o CPF do cliente (num cenário real, isso seria o equivalente a pôr o CPF na nota fiscal)
            purchase['purchaser_name'] = input("Informe o nome do cliente: ")
            purchase['purchaser_cpf'] = ipt.input_cpf("Informe o CPF do cliente: ")
        response = r.post(f'purchases/{purchase_id}/pay', HEADERS, purchase)
        r.render_response_message(response)
        if r.is_success(response):
            menu.render_purchase(response.json().get('data'))
            return True
    return False

def cancel_purchase(purchase_id):
    """Cancela a última compra que foi registrada pelo caixa
    Returns:
        Retorna True em caso de sucesso ou False em caso de falha ou cancelamento
    """
    if input("Para confirmar o cancelamento da compra, insira 'Y': ").upper() == 'Y':
        response = r.post(f'purchases/{purchase_id}/cancel', HEADERS)
        r.render_response_message(response)
        return r.is_success(response)
    return False

def check_cashier_situation():
    """Consulta a situação do caixa (isso inclui informações sobre IP, Id e dados da ultima compra)"""
    response = r.post('cashiers/register', HEADERS)
    if r.is_success(response):
        print("Situação consultada com sucesso!")
        menu.render_cashier(response.json().get('data'))
    else:
        print("Falha ao consultar situação!")