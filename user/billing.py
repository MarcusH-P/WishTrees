import random


def valid_payment(money_amount, card_number):
    # This is where a bank API would be use to approve of the

    # The percentage chance the card will fail
    fail_chance = 30

    # Gives the users card a chance to fail
    if random.randint(0, 100) >= fail_chance:
        return False
    return True
