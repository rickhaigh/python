import random
import sqlite3

# conn = sqlite3.connect(':memory:')
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()


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
        cur.execute("INSERT INTO card (id, number, pin, balance) VALUES (?, ?, ?, ?);", (self.id, self.card_num, str(self.pin), self.balance))
        conn.commit()

        #print("Your card has been created")
        #print("Your card number")
        print(self.card_num)
        #print("Your card PIN:")
        #print(self.pin)
        #print()


random.seed(57)
menu_choice = 0
menu_choice2 = 0

# for _ in range(0, 10):
#    card1 = CreditCard()

cur.execute("SELECT id, number, pin, balance FROM card;")
results = cur.fetchall()
for item in results:
    print(item)

conn.close()