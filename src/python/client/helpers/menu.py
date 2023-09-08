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

def render_purchase(purchase):
    print(f"\tID: {purchase['id']}")
    print(f"\tSituação: {TRANSLATED_PURCHASE_STATUS[purchase['total_value']]}")
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

def render_cashier(cashier):
    print(f"Exibindo informações para o caixa {cashier['id']}:")
    print(f"\tID: {cashier['id']}")
    print(f"\tIP: {cashier['ip']}")
    print(f"\tBloqueado: {'Sim' if cashier['is_blocked'] else 'Não'}")
    print(f"\tQuantidade de compras registradas: {len(cashier['registered_purchases'])}")
    scroll_console(2)