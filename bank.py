import random


class Account:
    def __init__(self):
        # Generate PIN number
        self.pin = random.randint(10**(4-1), (10**4)-1)
        # Generate card number
        self.iin = 400000
        self.can = random.randint(10**(16-1), (10**16)-1)
        self.checksum = 1  # Will need to generate later using Luhn algo
        self.card_num = int(str(self.iin) + str(self.can) + str(self.checksum))


# Present user with menu
print('1. Create an account')
print('2. Log into account')
print('0. Exit')

while True:
    user_input = input()
    if user_input == "0":
        print("Bye!")
        break
    elif user_input == "1":
        new_card = Account()

        print("Your card has been created")
        print("Your card number:")
        print(new_card.card_num)
        print("Your card PIN:")
        print(new_card.pin)
