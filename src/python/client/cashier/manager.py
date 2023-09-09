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
            return menu.render_purchase(response.json().get('data'))
        return None
    else:
        print("Compra cancelada!")
        return None

def pay_purchase(purchase_id):
    return True