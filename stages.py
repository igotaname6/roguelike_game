from inventory_creator import import_inventory
import operator
import random
import os   # for screen clearing
import datetime  # for time counting
import csv
import sys   # for getch() function
import tty
import termios

color_black = '\033[3;30;40m'
color_red = '\033[3;31;41m'   # jak powinny być przechowywane barwy??
color_green = '\033[3;32;42m'
color_yellow = '\033[3;33;43m'
color_blue = '\033[3;34;44m'
color_purple = '\033[3;35;45m'
color_cyan = '\033[3;36;46m'
color_white = '\033[3;37;47m'
color_normal = '\033[1;37;0m'
color_character = '\033[1;31;47m'


def getch():    # WASD moving
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)  # wczytaj z systemu, z podstawowego wejscia, jeden znak
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def create_board(filename='board1.csv'):
    """reads game_board from csv file, and save all characters  in nested list"""
    with open(filename, mode='r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        board = []
        for row in reader:
            board.append(row)
    return board    # return nested list [y][x]


def print_board(board):
    """prints board on the screen and colouring by characters"""
    for horizon in range(len(board)):
        for vertical in range(len(board[horizon])):
            if board[horizon][vertical] == 'ź':
                print(color_white + ' ' + color_normal, end='')
            elif board[horizon][vertical] == 'ł':
                print(color_green + ' ' + color_normal, end='')
            elif board[horizon][vertical] == 'ń':
                print(color_blue + ' ' + color_normal, end='')
            elif board[horizon][vertical] == 'ż':
                print(color_black + ' ' + color_normal, end='')
            elif board[horizon][vertical] == 'drzwi':
                print(color_red + ' ' + color_normal, end='')
            elif board[horizon][vertical] == 'Θ':
                print(color_character + board[horizon][vertical] + color_normal, end='')
            elif board[horizon][vertical] == '':
                print(color_yellow + ' ' + color_normal, end='')
            elif board[horizon][vertical] == '*':
                print(' ', end='')
            else:
                print(board[horizon][vertical], end='')
        print()


def insert_player(board, x, y):
    """inserts avatar on the screen in game board"""
    board[y][x] = ('Θ')
    return board


def add_to_inventory(inventory, added_items):
    '''Adds to the inventory dictionary a list of items from added_items.'''
    for i in range(len(added_items)):
        if added_items[i] in inventory:
            inventory[added_items[i]] += 1
        else:
            inventory[added_items[i]] = 1


def print_table(inventory, order=None):
    '''Takes your inventory and displays it in a well-organized table with
    each column right-justified. The input argument is an order parameter (string)
    which works as the following:
    - None (by default) means the table is unordered
    - "count,desc" means the table is ordered by count (of items in the inventory)
      in descending order
    - "count,asc" means the table is ordered by count in ascending order.'''
    if order is None:
        items_number = 0
        for key in inventory:
            items_number += inventory[key]
        max_key_length = max(map(len, inventory))
        print('Inventory:')
        print('  count    \b', ' '*(max_key_length-9), '\bitem name')
        print('-' * (11 + max_key_length))
        for key in inventory:
            print(' ' * (6-len(str(inventory[key]))), inventory[key], ' ',
                  ' ' * (max_key_length - len(key)), key)
        print('-' * (11 + max_key_length))
        print('Total number of items:', items_number)
    else:
        items_number = 0
        for key in inventory:
            items_number += inventory[key]
        max_key_length = max(map(len, inventory))
        if order == 'count,desc':
            type_of_sort = True
        elif order == 'count,asc':
            type_of_sort = False
        inventory_sorted = sorted(inventory.items(), key=operator.itemgetter(1), reverse=type_of_sort)
        # Sorting(copying) of dict, changing it to list of tuples.
        print('Inventory:')
        print('  count    \b', ' '*(max_key_length-9), '\bitem name')
        print('-' * (11 + max_key_length))
        for i in range(len(inventory_sorted)):
            print(' ' * (6-len(str(inventory_sorted[i][1]))), inventory_sorted[i][1], ' ',
                  ' ' * (max_key_length - len(inventory_sorted[i][0])), inventory_sorted[i][0])
        print('-' * (11 + max_key_length))
        print('Total number of items:', items_number)
        print('-' * (11 + max_key_length))
        print('Press P to exit')


def user_command(key_input, x, y, board):
    """reads command from keybords and interact with game"""
    obstacles = ['ź', 'ł', 'ń', 'ż', 'ó']
    broadcast = None
    if key_input == 'p':  # exit from game
        exit()
    elif key_input == 'w':  # move avatr upward
        y -= 1
        if board[y][x] in obstacles:
            y += 1
    elif key_input == 'a':  # move character left
        x -= 1
        if board[y][x] in obstacles:
            x += 1
    elif key_input == 's':  # move down
        y += 1
        if board[y][x] in obstacles:
            y -= 1
    elif key_input == 'd':  # move right
        x += 1
        if board[y][x] in obstacles:
            x -= 1
    elif key_input == 'e':  # show inventory
        broadcast = "change"
        return x, y, broadcast
    if x == 3 and y == 4:
        broadcast = "drzwi1"
    if x == 20 and y == 29:
        broadcast = 'budynek1'
    return x, y, broadcast


def main():
    os.system('clear')
    '''Intro screen. '''
    while True:
        os.system('clear')
        print_board(create_board("intro.csv"))
        key_input = getch()
        if key_input == 'a':    # about screen
            os.system('clear')
            print_board(create_board("about.csv"))
            key_input = getch()
        elif key_input == 'h':    # how-to-play screen
            os.system('clear')
            print_board(create_board("howtoplay.csv"))
            key_input = getch()
        elif key_input == 'f':    # highscore screen
            os.system('clear')
            print_board(create_board("highscore.csv"))
            key_input = getch()
        elif key_input == 'x':  # move to game
            break
        elif key_input == 'p':
            exit()

    '''Create character screen. '''
    os.system('clear')
    print_board(create_board('character_choose.csv'))
    key_input = None
    while key_input not in ["t", "n", "p"]:
        key_input = getch()
        if key_input == 't':    # for terrorist
            broadcast_character_choice = 'terror'
        elif key_input == 'n':      # for navy
            broadcast_character_choice = 'navy'
        elif key_input == 'p':
            exit()

    '''First stage. '''
    os.system('clear')
    game_factors = [2, 2]  # starting position # list with factors depending on game progress
    board_change = "board1.csv"
    state_drzwi1 = 'inside'
    inventory = {'rope': 1, 'torch': 6, 'gold coin': 42, 'dagger': 1, 'arrow': 12}

    while True:
        interactions_on_board = insert_player(create_board(board_change), game_factors[0], game_factors[1])
        print_board(interactions_on_board)
        print_table(inventory, "count,desc")

        print(game_factors)     # testowo
        key_input = getch()
        game_factors = user_command(key_input, game_factors[0], game_factors[1], interactions_on_board)

        if game_factors[2] is None:
            board_change = "board1.csv"   # do napsania funkcja zmieniająca plansze.

        elif game_factors[2] is "change":
            board_change = "menu.csv"

        elif game_factors[2] is 'drzwi1':
            # os.system('clear')
            question_door1 = input('2 + 2 = ')
            while question_door1 != '4':
                question_door1 = input('2 + 2 = ')
            if state_drzwi1 == 'inside':
                game_factors = [3, 5]
                state_drzwi1 = 'outside'
            else:
                game_factors = [3, 3]
                state_drzwi1 = 'inside'
            os.system('clear')

        elif game_factors[2] is 'budynek1':
            exit()

        os.system('clear')

    '''Highscore.'''


if __name__ == '__main__':
    main()
