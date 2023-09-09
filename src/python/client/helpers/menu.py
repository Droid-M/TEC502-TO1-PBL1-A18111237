import os
import sys
import subprocess
import locale
import pytz
from datetime import datetime

try:
    locale.setlocale(locale.LC_ALL, 'portuguese_brazil')
except locale.Error:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

TRANSLATED_PAYMENT_METHODS = {
    'pix': 'Pix',
    'cash': 'Dinheiro',
    'credit_card': 'Cartão de crédito',
    None: '(Nenhuma forma de pagamento definida)'
}

TRANSLATED_PURCHASE_STATUS = {
    'started': 'Iniciada',
    'paid': 'Paga',
    'canceled': 'Cancelada',
    None: '(Nenhum status definido para a compra)'
}

def to_brazil_time(database_value):
    try:
        dt = datetime.strptime(database_value, '%Y-%m-%d %H:%M:%S')
        brasilia_timezone = pytz.timezone('America/Sao_Paulo')
        return pytz.utc.localize(dt).astimezone(brasilia_timezone)
    except ValueError:
        return datetime.strptime(database_value, '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y às %H:%M:%S')

def restart():
    print("Reiniciando programa...")
    command = [sys.executable] + sys.argv
    subprocess.Popen(command, creationflags=subprocess.CREATE_NEW_CONSOLE)
    sys.exit()

def close():
    print("Saindo do programa...")
    exit()

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def scroll_console(lines = 10):
    for _ in range(lines):
        print()

def pause():
    return input("Pressione Enter para continuar...")

def float_to_currency(value):
    return locale.currency(value, grouping = True, symbol = True)

def render_product(product):
    print(f"\tID: {product['id']}")
    print(f"\tNome: {product['name']}")
    print(f"\tQuantidade em estoque: {product['stock_quantity']}")
    print(f"\tCódigo: {product['bar_code']}")
    print(f"\tPreço: {float_to_currency(product['price'])}")
    print(f"\tCadastrado em: {to_brazil_time(product['created_at'])}")
    scroll_console(2)

def render_products(products):
    for i in products:
        render_product(products[i])

def render_purchase(purchase):
    print(f"\tID: {purchase['id']}")
    print(f"\tSituação: {TRANSLATED_PURCHASE_STATUS[purchase['status']]}")
    print(f"\tValor total: {float_to_currency(purchase['total_value'])}")
    print(f"\tNome do comprador: {purchase['purchaser_name'] if purchase['purchaser_name'] else '(Não informado)'}")
    print(f"\tCPF do comprador: {purchase['purchaser_cpf'] if purchase['purchaser_cpf'] else '(Não informado)'}")
    print(f"\tForma de pagamento: {TRANSLATED_PAYMENT_METHODS[purchase['payment_method']]}")
    print(f"\tQuantidade de produtos: {len(purchase['products'])}")
    print(f"\tID do caixa que processou: {purchase['origin_cashier']}")
    print(f"\tIniciada em: {to_brazil_time(purchase['created_at'])}")
    scroll_console(2)

def render_purchases(purchases):
    for i in purchases:
        render_purchase(purchases[i])
    if (input("Insira 'Y' para consultar detalhes sobre os produtos usados em alguma das compras listadas ou insira qualquer outro valor para ver as próximas ações: ").upper() == 'Y'):
        id = input("Insira o ID da compra: ")
        if id in purchases:
            render_products(purchases[id]['products'])
        else:
            print("O ID informado não pertence a nenhuma das compras listadas anteriormente!")

def render_cashier(cashier):
    print(f"Exibindo informações para o caixa {cashier['id']}:")
    print(f"\tID: {cashier['id']}")
    print(f"\tIP: {cashier['ip']}")
    print(f"\tBloqueado: {'Sim' if cashier['is_blocked'] else 'Não'}")
    print(f"\tQuantidade de compras registradas: {len(cashier['registered_purchases'])}")
    scroll_console(2)

def render_cashiers(cashiers):
    for i in cashiers:
        render_cashier(cashiers[i])
    if (input("Insira 'Y' para consultar detalhes sobre as compras efetuadas por algum dos caixas ou insira qualquer outro valor para ver as próximas ações: ").upper() == 'Y'):
        id = input("Insira o ID do caixa: ")
        if id in cashiers:
            render_purchases(cashiers[id]['registered_purchases'])
        else:
            print("O ID informado não pertence a nenhum dos caixas listados anteriormente!")