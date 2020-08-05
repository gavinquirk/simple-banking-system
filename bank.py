import random
import sqlite3

# Global Vars
current_account = None

# Database Connection
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()

# Create database if it doesn't already exist
cur.execute("""CREATE TABLE IF NOT EXISTS card (
        id INTEGER,
        number TEXT,
        pin TEXT,
        balance INTEGER DEFAULT 0
    );
""")
conn.commit()


class Account:
    def __init__(self):
        self.pin = gen_rand_number_given_size(4)
        self.iin = 400000
        self.can = gen_rand_number_given_size(9)
        self.checksum = generate_checksum(self.iin, self.can)
        self.card_num = int(str(self.iin) + str(self.can) + str(self.checksum))
        self.balance = 0
        cur.execute("INSERT INTO card (number, pin) VALUES ('{0}', '{1}')".format(
            str(self.card_num), str(self.pin)))
        conn.commit()


def generate_checksum(iin, can):
    # Get list of nums
    partial_card = int(str(iin) + str(can))
    partial_list = [int(i) for i in str(partial_card)]
    # Reverse order
    partial_reversed = partial_list[::-1]
    partial_doubled = []
    partial_added = []
    counter = 0

    # Double every second digit
    for num in partial_reversed:
        if (counter % 2 == 0):
            num = num * 2
            partial_doubled.append(num)
            counter += 1
        else:
            partial_doubled.append(num)
            counter += 1

    # If digit is more than 9, add the digits together
    for num in partial_doubled:
        if num > 9:
            num1 = [int(d) for d in str(num)][0]
            num2 = [int(d) for d in str(num)][1]
            new_num = num1 + num2
            partial_added.append(new_num)
        else:
            partial_added.append(num)

    # Add all numbers together
    total = sum(partial_added)
    multiplied = total * 9
    check_digit = multiplied % 10
    return check_digit


def validate_checksum(card_number):
    iin = 400000
    can = int(card_number[6:15])
    check_digit = int(card_number[-1])
    generated_check_digit = generate_checksum(iin, can)
    if check_digit == generated_check_digit:
        return True
    else:
        return False


def gen_rand_number_given_size(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return random.randint(range_start, range_end)


def log_in(card_num, pin):
    # Get card info from db
    cur.execute("""SELECT number, pin FROM card WHERE number={0} AND pin={1}""".format(
        card_num, pin))
    result = cur.fetchone()
    # If no result exists (returns None), tell user. If result does exist, log in
    if result == None:
        print('Wrong card number or PIN!')
    else:
        global current_account
        current_account = card_num
        print('You have successfully logged in!')


while True:
    # Present user with menu
    if current_account == None:
        print('1. Create an account')
        print('2. Log into account')
        print('0. Exit')
    else:
        print('1. Balance')
        print('2. Add Income')
        print('3. Do transfer')
        print('4. Close account')
        print('5. Log out')
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
    # Check balance condition
    elif user_input == '1' and current_account != None:
        # Query DB for account balance
        cur.execute(
            """SELECT balance FROM card WHERE number={0}""".format(current_account))
        result = cur.fetchone()
        print('Balance: ' + str(result[0]))
    # Add Income condition
    elif user_input == '2' and current_account != None:
        print('Enter income:')
        income = input()
        cur.execute("""UPDATE card SET balance={0} WHERE number={1}""".format(
            income, current_account))
        conn.commit()
        print('Income was added!')
    # Do transfer condition
    elif user_input == '3' and current_account != None:
        cur.execute(
            """SELECT balance FROM card WHERE number={0}""".format(current_account))
        current_balance = cur.fetchone()[0]
        print('Transfer')
        print('Enter card number:')
        target_number = input()
        # If target number does not pass Lunh algo,
        # tell user there is a mistake in card num
        if not validate_checksum(target_number):
            print("Probably you made mistake in the card number. Please try again!")
        # If target number is same as current account number
        elif int(target_number) == current_account:
            print("You can't transfer money to the same account!")

        # Get amount to transfer
        print('Enter how much money you want to transfer:')
        target_amount = int(input())
        # If user tries to transfer more money than they have,
        # print warning message.
        if target_amount > current_balance:
            print('Not enough money!')

    # Close account condition
    # Log out condition
    elif user_input == '5' and current_account != None:
        current_account = None
        print('You have successfully logged out!')


# Commit db changes
conn.commit()
