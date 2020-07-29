import random

# All cards which have been created
all_cards = {}
current_account = 'none'


class Account:
    def __init__(self):
        # Generate PIN number
        self.pin = random.randint(10**(4-1), (10**4)-1)
        # Generate card number
        self.iin = 400000
        self.can = random.randint(10**(16-1), (10**16)-1)
        self.checksum = 1  # Will need to generate later using Luhn algo
        self.card_num = int(str(self.iin) + str(self.can) + str(self.checksum))
        all_cards.update({self.card_num: self.pin})


while True:
    # Present user with menu
    if current_account == 'none':
        print('1. Create an account')
        print('2. Log into account')
        print('0. Exit')
    else:
        print('1. Balance')
        print('2. Log out')
        print('0. Exit')

    user_input = input()
    # Exit condition
    if user_input == "0":
        print("Bye!")
        break
    # Create account condition
    elif user_input == "1" and current_account == 'none':
        new_account = Account()
        current_account = new_account.card_num
        print("Your card has been created")
        print("Your card number:")
        print(new_account.card_num)
        print("Your card PIN:")
        print(new_account.pin)
    # Log in condition
    elif user_input == "2" and current_account == 'none':
        print('Enter your card number:')
        card_num = int(input())
        print('Enter your PIN:')
        pin = int(input())
        # If card number is found, and pin is correct, log in
        if card_num in all_cards and all_cards[card_num] == pin:
            current_account = card_num
            print('You have successfully logged in!')
        else:
            print('Wrong card number or PIN!')
    # Log out condition
    elif user_input == '2' and current_account != 'none':
        current_account = 'none'
        print('You have successfully logged out!')
