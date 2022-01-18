import random


def valid_payment():
    if random.randint(0, 100) <= 30:
        return False
    return True
