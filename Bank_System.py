# Author: 	   Fionn O'Reilly
# Filename:    Bank_System.py
# Description: Presenting the user with a menu to create/close a bank account,
# 			   withdraw or deposit from/to account, or print details of all accounts.
# 			   Program reads current bank account details from a file and separates them into lists.
# 			   Lists are then edited based on user actions, the updated information is then sent back to the file.
# 			   All user input is validated.


from random import randint


# Reading all bank account details from file
def read_file():
    number_list = []
    balance_list = []
    fname_list = []
    lname_list = []
    bank_details = open('bank.txt', 'r')
    bank_details = bank_details.readlines()
    # Separating file information into lists of account numbers, account balance, first name, and surname
    for line in bank_details:
        line = line.split()
        number_list.append(int(line[0]))
        balance_list.append(float(line[1]))
        fname_list.append(line[2])
        lname_list.append(line[3])
    return number_list, balance_list, fname_list, lname_list


# Checking that the user entered a number from 1 to 6
def validate_menu_choice(prompt):
    valid_input = False
    while valid_input is False:
        try:
            user_input = int(input(prompt))
            if user_input < 1 or user_input > 6:
                print('ERROR - Please enter a number from 1 to 6')
            else:
                valid_input = True
        except:
            print('ERROR - Please enter a number from 1 to 6')
    return user_input


# Checking that the account number assigned to a newly opened account does not already exist
def check_for_existing_number(number, number_list):
    valid_number = False
    while valid_number is False:
        # Generating a new random 5 digit account number if the previous account number already exists
        if number in number_list:
            number = '{:05}'.format(randint(0, 99999))
        else:
            account_number = number
            valid_number = True
    return account_number


# Checking that first name and surname are letters and are at least 2 characters long
def validate_name(prompt):
    valid_fname = False
    while valid_fname is False:
        name = input(prompt)
        name = name.replace(' ', '\'')
        length = len(name)
        if not name.isalpha():
            # Allowing for apostrophes in surnames
            if '\'' in name and length >= 2:
                valid_fname = True
            else:
                print('ERROR - Name must be letters only')
        elif length < 2:
            print('ERROR - Name must be at least two characters long')
        else:
            valid_fname = True
    return name


# Checking that the account number given by the user exists when withdrawing/depositing money or closing an account
def check_account_number(prompt, number_list):
    valid_number = False
    while valid_number is False:
        try:
            account_number = int(input(prompt))
            if account_number not in number_list:
                print('ERROR - Account number does not exist')
            else:
                valid_number = True
        except:
            print('ERROR - Invalid account number')
    return account_number


# Checking that withdrawal amount entered by user contains numbers only and isn't larger than account balance
def check_withdrawal_amount(prompt, acc_num_position, balance_list):
    withdrawal_amount = 0
    MIN_WITHDRAWAL = 10
    valid_withdrawal = False
    while valid_withdrawal is False:
        # noinspection PyBroadException
        try:
            account_balance = balance_list[acc_num_position]
            withdrawal_amount = int(input(prompt))
            if withdrawal_amount > account_balance:
                print('Insufficient funds')
            elif withdrawal_amount < MIN_WITHDRAWAL:
                print('ERROR - Withdrawal amount cannot be less than €10')
            else:
                valid_withdrawal = True
        except Exception:
            print('ERROR - Please enter numbers only')
    return withdrawal_amount


# Checking that deposit amount entered by user is a number and does not exceed deposit limit
def validate_deposit(prompt):
    deposit_amount = 0
    MAX_LIMIT = 20000
    MIN_DEPOSIT = 10
    valid_deposit = False
    while valid_deposit is False:
        # noinspection PyBroadException
        try:
            deposit_amount = int(input(prompt))
            if deposit_amount > MAX_LIMIT:
                print('ERROR - Deposit cannot exceed €20,000')
            elif deposit_amount < MIN_DEPOSIT:
                print('ERROR - Deposit amount cannot be below €10')
            else:
                valid_deposit = True
        except Exception:
            print('ERROR - Please enter numbers only')
    return deposit_amount


# Displaying main menu and taking user's menu choice
def menu_select(prompt):
    menu = '\n1. Open an account \
          \n2. Close an account \
          \n3. Withdraw money \
          \n4. Deposit money \
          \n5. Generate a report for management \
          \n6. Quit\n'
    print(menu)
    menu_choice = validate_menu_choice(prompt)
    print()
    return menu_choice


# Generating new five digit account number, taking account holder's name, and appending new details to lists
def open_account(number_list, balance_list, fname_list, lname_list):
    account_number = check_for_existing_number('{:05}'.format(randint(0, 99999)), number_list)
    print('Your new account number: ', account_number)
    number_list.append(account_number)
    balance_list.append(0.0)
    account_holder_fname = validate_name('Enter your first name: ')
    fname_list.append(account_holder_fname)
    account_holder_lname = validate_name('Enter your surname: ')
    lname_list.append(account_holder_lname)
    print('Account created')
    return_to_menu = True
    return return_to_menu


# Getting account number from user and deleting correpsonding details from all lists
def close_account(number_list, balance_list, fname_list, lname_list):
    account_number = check_account_number('Enter account number: ', number_list)
    acc_num_position = number_list.index(account_number)
    number_list.remove(number_list[acc_num_position])
    balance_list.remove(balance_list[acc_num_position])
    fname_list.remove(fname_list[acc_num_position])
    lname_list.remove(lname_list[acc_num_position])
    print('Account closed')
    return_to_menu = True
    return return_to_menu


# Getting account number and withdrawal amount from user,
# subtracting amount from balance associated with account,
# and replacing old balance in list with new balance
def withdraw_money(number_list, balance_list):
    account_number = check_account_number('Enter account number: ', number_list)
    acc_num_position = number_list.index(account_number)
    withdrawal_amount = check_withdrawal_amount('Enter amount to withdraw: ', acc_num_position, balance_list)
    old_balance = balance_list[acc_num_position]
    new_balance = balance_list[acc_num_position] - withdrawal_amount
    balance_list[balance_list.index(old_balance)] = new_balance
    print('Withdrawal successful')
    return_to_menu = True
    return return_to_menu


# Getting account number and deposit amount from user,
# adding deposit amount to balance associated with account,
# and replacing old balance in list with new balance
def deposit_money(number_list, balance_list):
    account_number = check_account_number('Enter account number: ', number_list)
    acc_num_position = number_list.index(account_number)
    deposit_amount = validate_deposit('Enter amount to deposit: ')
    old_balance = balance_list[acc_num_position]
    new_balance = balance_list[acc_num_position] + deposit_amount
    balance_list[balance_list.index(old_balance)] = new_balance
    print('Deposit successful')
    return_to_menu = True
    return return_to_menu


# Printing details of all accounts, total on deposit in the bank, and highest balance
def generate_report(number_list, balance_list, fname_list, lname_list):
    print('Acc No.\t\t' + 'Balance\t\t', '  Name')
    length = len(number_list)
    position = 0
    while position < length:
        print(str(number_list[position]) + '\t\t' + '€' + str(
            '{:<10}'.format(balance_list[position])) + '\t' + '{:<20}'.format(
            fname_list[position] + ' ' + lname_list[position]))
        position += 1
    print('\nTotal on deposit: ', '€' + str(sum(balance_list)))
    max_balance_position = balance_list.index(max(balance_list))
    max_balance_holder = fname_list[max_balance_position].rstrip() + ' ' + lname_list[max_balance_position].rstrip()
    print('Max balance is', '€' + str(max(balance_list)), 'held by', max_balance_holder)
    return_to_menu = True
    return return_to_menu


# Writing account details from lists to file
def update_file(menu_choice, number_list, balance_list, fname_list, lname_list):
    bank_details = open('bank.txt', 'w')
    length = len(number_list)
    position = 0
    while position < length:
        account_details = str(number_list[position]), str(balance_list[position]), fname_list[position], lname_list[
            position]
        account_details = ' '.join(account_details)
        bank_details.write(account_details)
        bank_details.write('\n')
        position += 1
    bank_details.close()
    return_to_menu = True
    # Ending the program if the user chooses to quit
    if menu_choice == 6:
        print('Exiting...thank you!')
        exit()
    return return_to_menu


# Executing menu choice selected by user
def execute_choice(menu_choice, number_list, balance_list, fname_list, lname_list):
    if menu_choice == 1:
        open_account(number_list, balance_list, fname_list, lname_list)
    elif menu_choice == 2:
        close_account(number_list, balance_list, fname_list, lname_list)
    elif menu_choice == 3:
        withdraw_money(number_list, balance_list)
    elif menu_choice == 4:
        deposit_money(number_list, balance_list)
    elif menu_choice == 5:
        generate_report(number_list, balance_list, fname_list, lname_list)
    elif menu_choice == 6:
        update_file(menu_choice, number_list, balance_list, fname_list, lname_list)
    return menu_choice


def main():
    # Returning user to menu until they choose to quit
    return_to_menu = True
    while return_to_menu is True:
        number_list, balance_list, fname_list, lname_list = read_file()
        menu_choice = menu_select('Please choose a menu option by entering the corresponding number: ')
        execute_choice(menu_choice, number_list, balance_list, fname_list, lname_list)
        update_file(menu_choice, number_list, balance_list, fname_list, lname_list)


main()
