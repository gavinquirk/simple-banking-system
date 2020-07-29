import random

# Global Vars
current_account = None
all_accounts = {}


class Account:
    def __init__(self):
        self.pin = gen_rand_number_given_size(4)
        self.iin = 400000
        self.can = gen_rand_number_given_size(9)
        self.checksum = 1  # Will need to generate later using Luhn algo
        self.card_num = int(str(self.iin) + str(self.can) + str(self.checksum))
        self.balance = 0
        all_accounts.update({self.card_num: self})


def gen_rand_number_given_size(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return random.randint(range_start, range_end)


def log_in(card_num, pin):
    if all_accounts[card_num].pin == pin:
        global current_account
        current_account = all_accounts[card_num]
        print('You have successfully logged in!')
    else:
        print('Wrong card number or PIN!')


while True:
    # Present user with menu
    if current_account == None:
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
    elif user_input == "1" and current_account == None:
        new_account = Account()
        print("Your card has been created")
        print("Your card number:")
        print(new_account.card_num)
        print("Your card PIN:")
        print(new_account.pin)
    # Log in condition
    elif user_input == "2" and current_account == None:
        print('Enter your card number:')
        card_num = int(input())
        print('Enter your PIN:')
        pin = int(input())
        log_in(card_num, pin)
    # Log out condition
    elif user_input == '2' and current_account != None:
        current_account = None
        print('You have successfully logged out!')
    # Check balance condition
    elif user_input == '1' and current_account != None:
        print('Balance: ' + str(current_account.balance))
