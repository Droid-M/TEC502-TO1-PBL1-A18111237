from helpers import menu
from cashier import manage

def main(data):
    checkoutStatus = None
    while True:
        menu.scroll_console()
        print("Menu do caixa:")
        
        if checkoutStatus == None:
            print('1 - Escanear produtos')
            if not manage.cashier_is_locked():
                checkoutStatus = 'SCANNING_PRODUCTS'
                manage.scan_products()
        elif checkoutStatus == 'SCANNING_PRODUCTS':
            print('2 - Validar items da compra')
            
            checkoutStatus == ''