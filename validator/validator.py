def validate_password(password: str):
    digits = '1234567890'
    upper_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lower_letters = 'abcdefghijklmnopqrstuvwxyz'
    symbols = '!"#$%&\'()*+,-./:;<=>?@[]\\^_`{|}'
    acceptable = digits + upper_letters + lower_letters + symbols
    result = True
    symbol_counter = 0
    if len(password) < 8:
        print(f'длина не соответсвует длине  {8 - len(password)}')
        result = False
    for char in password:
        if char not in acceptable:
            result = False
    for char in password:
        if char in symbols:
            symbol_counter += 1
    if symbol_counter < 1:
        result = False
    return result

