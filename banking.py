import random
import sys
import sqlite3

# Initialise sqlite database
conn = sqlite3.connect("card.s3db")
c = conn.cursor()


# RESET TABLE IN DB ON EVERY RUN
def create_db():
    c.execute("DROP TABLE IF EXISTS card")
    c.execute("""CREATE TABLE IF NOT EXISTS card (
                id INTEGER,
                number TEXT,
                pin TEXT,
                balance INTEGER DEFAULT 0
                )""")
    conn.commit()


# Add a newly created card to the database
def add_to_db(number, pin):
    c.execute("SELECT MAX(id) from card")
    largest_id = c.fetchall()
    if largest_id[0][0] is not None:
        largest_id = largest_id[0][0] + 1
        # c.execute("INSERT INTO card VALUES (?, ?, ?, ?)", (largest_id, number, pin, 0))
        c.execute("INSERT INTO card VALUES (:id, :number, :pin, :balance)",
                  {"id": largest_id, "number": number, "pin": pin, "balance": 0})
    else:
        # c.execute("INSERT INTO card VALUES (?, ?, ?, ?)", (0, number, pin, 0))
        c.execute("INSERT INTO card VALUES (:id, :number, :pin, :balance)",
                  {"id": 0, "number": number, "pin": pin, "balance": 0})
    conn.commit()


# Add money to a card
def add_income(increase, card_numb):
    c.execute("SELECT balance FROM card WHERE number = (:number)",
                                {"number": card_numb})
    current_balance = c.fetchall()
    new_balance = current_balance[0][0] + increase
    c.execute("UPDATE card SET balance = (:balance) WHERE number = (:number)",
              {"balance": new_balance, "number": card_numb})
    conn.commit()


# Check balance of a card
def check_balance(card_numb):
    c.execute("SELECT balance FROM card WHERE number = (:num)",
              {"num": card_numb})
    balance = c.fetchall()
    print(balance[0][0])


# Check if card number entered on login is correct
def parse_db_numbers(card_number):
    c.execute("SELECT number FROM card")
    for x in c.fetchall():
        for y in x:
            if y == card_number:
                return True


# Check if card pin entered on login is correct
def parse_db_pins(card_number, pin):
    c.execute("SELECT pin FROM card WHERE number = (:card_num)",
              {"card_num": card_number})
    bank_pin = c.fetchall()
    if bank_pin[0][0] == pin:
        return True


# Delete a card
def close_account(card_number):
    c.execute("DELETE FROM card WHERE number = (:card_num)", {"card_num": card_number})
    conn.commit()
    print("\nThe account has been closed!")


# Creates a checksum for a 15 digit card number, to make a 16 digit card number
def luhn_algorithm(card_num):
    i, j, y, x = 0, 0, 0, 1
    num_list, num_list_2 = [], []

    # odd number positions (1, 3, 5, 7, 9, 11, 13, 15)
    while i < 16:
        num_list += card_num[i]
        i += 2
    odd_positions = list(map(int, num_list))
    while j <= 7:
        odd_positions[j] = odd_positions[j] * 2
        j += 1

    # even number positions (2, 4, 6, 8, 10, 12, 14)
    while x < 15:
        num_list_2 += card_num[x]
        x += 2
    even_positions = list(map(int, num_list_2))

    # if number > 9 in odd position list, minus 9
    for num in odd_positions:
        if num > 9:
            num = num - 9
            odd_positions[y] = num
        y += 1

    # sum odd (doubled) and even number positions
    sum_of_numbers = sum(odd_positions)
    sum_of_numbers += sum(even_positions)

    # create checksum (last digit)
    if (sum_of_numbers % 10) != 0:
        checksum = 0
        while (sum_of_numbers + checksum) % 10 != 0:
            checksum += 1
    elif (sum_of_numbers % 10) == 0:
        checksum = 0

    return str(checksum)


# Transfer funds from one card to another
def transfer_funds(transfer_to, transfer_from):
    c.execute("SELECT balance FROM card WHERE number = (:xfer_num)", {"xfer_num": transfer_to})
    check_list = c.fetchall()
    c.execute("SELECT balance FROM card WHERE number = (:xfer_num)", {"xfer_num": transfer_from})
    check_list2 = c.fetchall()
    if transfer_to == transfer_from:
        print("You can't transfer money to the same account!")
    elif luhn_algorithm(transfer_to[0:15]) != transfer_to[15]:
        print("Probably you made mistake in the card number. Please try again!")
    elif len(check_list) == 0:
        print("Such a card does not exist")
    elif len(check_list) != 0:
        print("Enter how much money you want to transfer:")
        transfer_amount = int(input())
        if transfer_amount > check_list2[0][0]:
            print("Not enough money!")
        else:
            # Add sum to "transfer to" account
            plus_balance = check_list[0][0] + transfer_amount
            c.execute("UPDATE card SET balance = (:new_bal) WHERE number = (:transfer_to)",
                      {"new_bal": plus_balance, "transfer_to": transfer_to})
            # Take off sum from current account
            c.execute("SELECT balance FROM card WHERE number = (:xfer_from)",
                      {"xfer_from": transfer_from})
            current_acc_bal = c.fetchall()
            minus_balance = current_acc_bal[0][0] - transfer_amount
            c.execute("UPDATE card SET balance = (:new_bal) WHERE number = (:transfer_from)",
                      {"new_bal": minus_balance, "transfer_from": transfer_from})
            conn.commit()
            print("Success!")


# Create a new card
def create_an_account():
    identifier_num = "400000"
    account_num = str(random.randint(0, 9))
    pin = ""
    while len(account_num) < 9:
        account_num += str(random.randint(0, 9))
    while len(pin) < 4:
        pin += str(random.randint(0, 9))
    chk_sum = luhn_algorithm(identifier_num + account_num)
    card_num = identifier_num + account_num + chk_sum
    add_to_db(card_num, pin)
    # c.execute("SELECT * from card")
    # print(c.fetchall())
    print("\nYour card has been created")
    print("Your card number:\n%s" % card_num)
    print("Your card PIN:\n%s" % pin)
    return identifier_num, account_num, chk_sum, card_num, pin


# Log onto a card
def log_into_account(card_num, pin):
    print("\nEnter your card number:")
    card_number_input = input()
    print("Enter your PIN:")
    pin_input = input()
    if parse_db_numbers(card_number_input) and\
            parse_db_pins(card_number_input, pin_input):
        print("\nYou have successfully logged in!")
        while True:
            print("\n1. Balance\n2. Add income\n3. Do transfer\n4. Close Account\n5. Log out\n0. Exit")
            choice_2 = input()
            if choice_2 == "1":
                print("\nBalance: ")
                check_balance(card_number_input)
            elif choice_2 == "2":
                print("\nEnter income:")
                add_money = int(input())
                add_income(add_money, card_number_input)
                print("Income was added!")
            elif choice_2 == "3":
                print("\nTransfer\nEnter card number:")
                transfer_to = input()
                transfer_funds(transfer_to, card_number_input)
            elif choice_2 == "4":
                close_account(card_number_input)
                break
            elif choice_2 == "5":
                print("\nYou have successfully logged out!")
                break
            elif choice_2 == "0":
                print("\nBye!")
                sys.exit()
    else:
        print("\nWrong card number or PIN!")


# Uses all of the above functions to finalise the Simple Banking System
create_db()
while True:
    print("\n1. Create an account\n2. Log into account\n0. Exit")
    choice = input()
    if choice == "1":
        IIN, account_number, checksum, card_number, PIN = create_an_account()
    elif choice == "2":
        log_into_account(card_number, PIN)
    elif choice == "0":
        print("\nBye!")
        conn.close()
        break

