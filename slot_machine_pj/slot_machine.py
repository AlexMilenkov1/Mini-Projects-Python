import random

MAX_LINES = 3
MAX_BET = 1000
MIN_BET = 10

ROWS = 3
COLS = 3

symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}

symbol_value = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2
}


def check_winnings(columns, lines, bet, values):
    winnings = 0
    winnings_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += 1
            winnings_lines.append(line + 1)

        return winnings, winnings_lines


def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, symbols in symbols.items():
        for _ in range(symbols):
            all_symbols.append(symbol)

    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)

        columns.append(column)

    return columns


def print_slot_machine(columns):
    for row in range(len(columns[0])):
        for index, column in enumerate(columns):
            if index != len(columns) - 1:
                print(column[row], end=" | ")
            else:
                print(column[row], end="")

        print()


def deposit():
    while True:
        amount = input("What amount of money would you like to deposit? $")

        if amount.isdigit():
            amount = int(amount)

            if amount > 0:
                break
            else:
                print("Please enter a number greater than zero!")

        else:
            print("Please enter a number!")
    return amount


def get_number_of_lines():
    while True:
        lines = input(f"Enter the number of lines you want to bet on (1 - {str(MAX_LINES)}): ")

        if lines.isdigit():
            lines = int(lines)

            if 1 <= lines <= MAX_LINES:
                break
            else:
                print("Please enter a valid number for lines!")

        else:
            print("Please enter a number!")
    return lines


def get_bet():
    while True:
        bet = input("What amount of money would you like to bet on each line? $")

        if bet.isdigit():
            bet = int(bet)

            if MIN_BET <= bet <= MAX_BET:
                break
            else:
                print(f"Please enter a number between {MIN_BET} - {MAX_BET}")

        else:
            print("Please enter a number!")
    return bet


def spin(balance):
    lines = get_number_of_lines()
    while True:
        bet = get_bet()
        total_bet = lines * bet

        if total_bet > balance:
            print(f"You don't have enough money in your balance, you balance is {balance}")
        else:
            break

    print(f"You are betting {bet}$ on {lines} lines. Total bet is equal to {total_bet}$")

    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    print(f"You won {winnings}.")
    print(f"You won on lines:", *winning_lines)
    return winnings - total_bet


def main():
    balance = deposit()
    while True:
        print(f"Your current balance is: {balance}")
        answer = input("Press enter to spin(q - quit)")
        if answer == "q":
            quit()
        balance += spin(balance)


main()
