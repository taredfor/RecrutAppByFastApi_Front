import re

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

def validate_email(email: str):
    pattern = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$" # TODO:исправить валидацию приема кириллицы
    return bool(re.match(pattern, email))

def placeholder_validate(string: str):
    return True

def validate_second_password(main_password_str: str, second_password_str: str, ):
    if validate_password(main_password_str):
        if main_password_str == second_password_str:
            second_password_incorrect_label.value = "Password is equiles"
            second_password_incorrect_label.color = "Green"
        else:
            second_password_incorrect_label.value = "Password is not equiles"
            second_password_incorrect_label.color = "Red"
    else:
        second_password_incorrect_label.value = ""