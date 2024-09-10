import random
import string


def password_generator():
    letters = list(string.ascii_letters)
    symbols = list(string.punctuation)
    numbers = list(string.digits)


    random_letters = random.choices(letters, k=6)
    random_symbols = random.choices(symbols, k=6)
    random_numbers = random.choices(numbers, k=6)


    list_password = random_letters + random_numbers + random_symbols
    random.shuffle(list_password)

    password = ''.join(list_password)
    return password