import random


class Account:
    def __init__(self):
        # Generate PIN number
        self.pin = random.randint(10**(4-1), (10**4)-1)
        # Generate card number


# Present user with menu
print('1. Create an account')
print('2. Log into account')
print('0. Exit')

while True:
    user_input = input()
    if user_input == "0":
        print("Bye!")
        break
