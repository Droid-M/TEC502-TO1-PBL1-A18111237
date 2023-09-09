import re

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

def input_cpf(message):
    cpf = re.sub(r'[^0-9]', '', input(message))

    if len(cpf) != 11:
        print("CPF inválido!")
        return input_cpf(message)

    if cpf == cpf[0] * 11:
        print("CPF inválido!")
        return input_cpf(message)

    total = 0
    for i in range(9):
        total += int(cpf[i]) * (10 - i)
    remainder = total % 11
    digit1 = 0 if remainder < 2 else 11 - remainder

    total = 0
    for i in range(10):
        total += int(cpf[i]) * (11 - i)
    remainder = total % 11
    digit2 = 0 if remainder < 2 else 11 - remainder

    if int(cpf[9]) == digit1 and int(cpf[10]) == digit2:
        return cpf
    else:
        print("CPF inválido!")
        return input_cpf(message)