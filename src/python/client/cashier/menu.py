from helpers import menu

def main(data):
    can_scroll_console = False
    checkoutStatus = None
    while True:
        if can_scroll_console:
            menu.scroll_console()
        print("Menu do caixa:")
        
        if checkoutStatus == None:
            print('1 - Escanear produtos')
            checkoutStatus = 'SCANNING_PRODUCTS'
        # elif checkoutStatus == 'SCANNING_PRODUCTS':
            
        can_scroll_console = True
