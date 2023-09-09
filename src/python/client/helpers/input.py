def input_integer(message):
    number = input(message)
    try:
        return int(number)
    except ValueError:
        print("Entrada inválida! Insira apenas valors numéricos!")
        return input_number(message)
    
def input_number(message):
    number = input(message)
    try:
        return float(number)
    except ValueError:
        print("Entrada inválida! Insira apenas valors numéricos!")
        return input_number(message)