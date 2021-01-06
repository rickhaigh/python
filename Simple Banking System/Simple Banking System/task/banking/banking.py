import random
import sqlite3
import sys

conn = sqlite3.connect('card.s3db') # (':memory:') starts with a fresh DB every time in RAM
cur = conn.cursor()

# clears the table if there is anything in it
cur.execute('drop table if exists card')
conn.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS card (
            id INTEGER,
            number TEXT,
            pin TEXT,
            balance INTEGER DEFAULT 0
            );""")
conn.commit()


class CreditCard:
    def calc_checksum(self, number):
        # expect number to be a string so we can iterate over it
        # step 1 multiply odd digits by 2
        char = ""
        char_sum = 0
        for i in range(0, len(number)):
            if i % 2 == 0:
                # multiply odd numbers by 2
                new_num = int(number[i]) * 2
                # if number is greater than 9 subtract 9
                if new_num > 9:
                    new_num -= 9
                # store new calculated number
                char_sum += new_num
                char += str(new_num)
            else:
                char += number[i]
                char_sum += int(number[i])

        # determine checksum value
        checksum = 10 - (char_sum % 10)
        if checksum == 10:
            checksum = 0  # handle special case where checksum is 10
        # copy original account number so we can add the checksum to it
        char = number
        # copy checksum to account number
        char += str(checksum)
        return int(char)

    def __init__(self):
        #          123456
        self.BIN = 400000
        #                                 7890123456
        #                                 1234567890
        self.account_num = random.randint(100000000,
                                          999999999)
        self.card_num = self.calc_checksum(str(self.BIN) + str(self.account_num))
        # self.checksum = self.card_num[len(self.card_num)]
        self.pin = random.randint(1, 9999)
        self.balance = 0
        self.id = self.account_num

        with conn:  # this context manager takes care of committing
            cur.execute("INSERT INTO card (id, number, pin, balance) VALUES (:id, :number, :pin, :balance);",
                        {'id': self.id, 'number': self.card_num, 'pin': str(self.pin), 'balance': self.balance})
        # conn.commit()

        print("Your card has been created")
        print("Your card number")
        print(self.card_num)
        print("Your card PIN:")
        print(self.pin)
        print()

    def make_deposit(self, value):
        self.balance += value
        # cur.execute("""SELECT """)

# end CLASS CreditCard


# Debug function
def print_db():
    cur.execute("SELECT * FROM card;")
    account_info_new = cur.fetchall()
    for item in account_info_new:
        print(item)
    print()





def check_balance(account_info):
    return account_info[3]


def add_income(account_info, deposit):
    balance = get_balance(account_info)
    deposit += balance
    with conn:
        cur.execute("""UPDATE card SET balance = :balance
                        WHERE number = :number AND pin = :pin;""",
                    {'number': account_info[1], 'pin': account_info[2], 'balance': deposit})
    print("Income was added!")


# Both accounts need to be verified before this function
def transfer(account_info_out, account_info_in, amount):
    if account_info_out[1] == account_info_in[1]:
        print("You can't transfer money to the same account!")
    elif account_info_out[3] < amount:
        # account has insufficient funds
        print("Not enough money!")
    else:
        # account looks good
        acct_in = account_info_in[3] + amount
        acct_out = account_info_out[3] - amount
        with conn:
            cur.execute("""UPDATE card SET balance = :balance
                                                WHERE number = :number AND pin = :pin;""",
                        {'number': account_info_out[1], 'pin': account_info_out[2], 'balance': acct_out})
            cur.execute("""UPDATE card SET balance = :balance
                                                WHERE number = :number AND pin = :pin;""",
                        {'number': account_info_in[1], 'pin': account_info_in[2], 'balance': acct_in})
        print("Success!")


def get_balance(account_info):
    cur.execute("SELECT * FROM card WHERE (number = :number);",
                {'number': account_info[1]})
    account_info_new = cur.fetchone()
    return account_info_new[3]


def close_account(account_info):
    with conn:
        cur.execute("DELETE from card WHERE number = :number AND pin = :pin",
                    {'number': account_info[1], 'pin': account_info[2]})
    print("The account has been closed!")


# need to pass in card number (not account record).  This function will strip off the checksum and recalculate it
def luhn_check(account_num):
    number = account_num[0:-1]  # strip off checksum character
    # expect number to be a string so we can iterate over it
    # step 1 multiply odd digits by 2
    char = ""
    char_sum = 0
    for i in range(0, len(number)):
        if i % 2 == 0:
            # multiply odd numbers by 2
            new_num = int(number[i]) * 2
            # if number is greater than 9 subtract 9
            if new_num > 9:
                new_num -= 9
            # store new calculated number
            char_sum += new_num
            char += str(new_num)
        else:
            char += number[i]
            char_sum += int(number[i])

    # determine checksum value
    checksum = 10 - (char_sum % 10)
    if checksum == 10:
        checksum = 0  # handle special case where checksum is 10
    # copy original account number so we can add the checksum to it
    char = number
    # copy checksum to account number
    char += str(checksum)
    return_val = account_num == char
    return return_val


def verify_account(account_number):
    # look for card number and pin
    cur.execute("SELECT * FROM card WHERE (number = :number);",
                {'number': account_number})
    account_info = cur.fetchone()
    if not account_info:
        return account_info
    else:
        return account_info

# MAIN #
random.seed(57)
menu_choice = 0
menu_choice2 = 0

# print_db()
while True:
    print()
    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")
    menu_choice = int(input())
    print()

    # card(
    #   id INTEGER,
    #   number TEXT,
    #   pin TEXT,
    #   balance INTEGER DEFAULT 0
    # )

    if menu_choice == 1:
        # create a new account
        card1 = CreditCard()
    elif menu_choice == 2:
        # try to log in
        print("Enter your card number:")
        card_num_in = input()
        print("Enter your PIN:")
        pin_num_in = input()

        # look for card number and pin
        cur.execute("SELECT * FROM card WHERE (number = :number) AND (pin = :pin);",
                    {'number': card_num_in, 'pin': pin_num_in})
        account = cur.fetchone()
        if account:
            card_num_check = card_num_in == account[1]
            card_pin_check = pin_num_in == account[2]
        else:
            print('Wrong card number or PIN!')
            continue
        if card_num_check and card_pin_check:
            # login was successful
            print("You have successfully logged in!")

            while True:
                print()
                print("1. Balance")
                print("2. Add income")
                print("3. Do transfer")
                print("4. Close account")
                print("5. Log out")
                print("0. Exit")
                menu_choice2 = int(input())
                print()

                if menu_choice2 == 1:
                    # check balance
                    balance = get_balance(account)
                    print(f'Balance: {balance}')

                elif menu_choice2 == 2:
                    # Add income
                    print("Enter income:")
                    income = int(input())
                    add_income(account, income)

                elif menu_choice2 == 3:
                    # Do transfer
                    print("Transfer")
                    print("Enter card number:")
                    account_num = input()
                    # verify account_num passes luhn_check
                    if luhn_check(account_num):
                        # verify account_num is in DB
                        account_in = verify_account(account_num)
                        if account_in:
                            print("Enter how much money you want to transfer:")
                            transfer_amount = int(input())
                            transfer(account, account_in, transfer_amount)
                        else:
                            print("Such a card does not exist.")
                    else:
                        # failed luhn check
                        print('Probably you made a mistake in the card number. Please try again!')

                elif menu_choice2 == 4:
                    # Close account
                    close_account(account)
                    break
                elif menu_choice2 == 5:
                    # log out of account
                    print("You have successfully logged out!")
                    break
                elif menu_choice2 == 0:
                    conn.close()
                    sys.exit('Bye!')

                # Update account in case anything changed
                cur.execute("SELECT * FROM card WHERE (number = :number) AND (pin = :pin);",
                            {'number': card_num_in, 'pin': pin_num_in})
                account = cur.fetchone()

            # while True (option 2)
        else:
            print("Probably you made a mistake in the card number. Please try again!")
            print()

    # main menu
    elif menu_choice == 0:
        conn.close()
        print("Bye!")
        break  # break out of while loop
# while True (main loop)
