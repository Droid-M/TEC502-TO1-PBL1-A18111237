from helpers import menu
from helpers import input as ipt
from helpers import file
from helpers import dict
from helpers import sensor
from helpers import request as r
import keyboard
import time

HEADERS = {
    'cashier-token': file.env('CASHIER_TOKEN'),
    'accept': 'application/json',
    'content': 'application/json'
}

async def check_cashier_block_status(data):
    response = r.get('', HEADERS)
    r.render_response_message(response)
    if r.is_success(response):
        data['cashier_locked'] = response.json().get('is_locked')


def cashier_is_locked():
    return

def scan_products():
    return sensor.receive_data()

def register_purchase(bar_codes):
    if input("Para prosseguir com a compra, insira 'Y': ").upper() == 'Y':
        response = r.post('', HEADERS, {'products_ids' : bar_codes})
        r.render_response_message(response)
        if r.is_success(response):
            print("Compra processada: ")
            menu.render_purchase(response.json().get('data'))
    else:
        print("Compra cancelada!")

def pay_purchase(purchase_id):
    return