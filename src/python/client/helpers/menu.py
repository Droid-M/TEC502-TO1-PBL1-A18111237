import os
import datetime

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

def sair():
    print("Saindo do programa.")
    exit()

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def scroll_console(lines = 10):
    for _ in range(lines):
        print()

def pause():
    return input("Pressione Enter para continuar...")

def render_product(product):
    print(f"\tID: {product['id']}")
    print(f"\tNome: {product['name']}")
    print(f"\tQuantidade em estoque: {product['stock_quantity']}")
    print(f"\tCódigo: {product['bar_code']}")
    print(f"\tPreço: {product['price']}")
    created_at = product['created_at']
    created_at = datetime.datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y às %H:%M:%S')
    print(f"\tCadastrado em: {created_at}")
    scroll_console(2)

def render_products(products):
    for i in products:
        render_product(products[i])

def render_purchase(purchase):
    print(f"\tID: {purchase['id']}")
    print(f"\tSituação: {TRANSLATED_PURCHASE_STATUS[purchase['status']]}")
    print(f"\tValor total: {purchase['total_value']}")
    print(f"\tNome do comprador: {purchase['purchaser_name'] if purchase['purchaser_name'] else '(Não informado)'}")
    print(f"\tCPF do comprador: {purchase['purchaser_cpf'] if purchase['purchaser_cpf'] else '(Não informado)'}")
    print(f"\tForma de pagamento: {TRANSLATED_PAYMENT_METHODS[purchase['payment_method']]}")
    print(f"\tQuantidade de produtos: {len(purchase['products'])}")
    print(f"\tID do caixa que processou: {purchase['origin_cashier']}")
    created_at = purchase['created_at']
    created_at =datetime.datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y às %H:%M:%S')
    print(f"\tIniciada em: {created_at}")
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