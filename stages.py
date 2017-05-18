from inventory_creator import import_inventory
import operator
import random
import os   # for screen clearing
import datetime  # for time counting
import csv   #
import sys   # for getch() function
import tty   #
import termios

color_black = '\033[3;30;40m'
color_red = '\033[3;31;41m'
color_green = '\033[3;32;42m'
color_yellow = '\033[3;33;43m'
color_blue = '\033[3;34;44m'
color_purple = '\033[3;35;45m'
color_cyan = '\033[3;36;46m'
color_white = '\033[3;37;47m'
color_normal = '\033[1;37;0m'
color_character = '\033[1;31;47m'
color_doors = '\033[1;30;41m'


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
    """Prints board on the screen and colouring by characters"""
    paint = {'ź': (color_white, ' '),
             'ł': (color_green, ' '),
             'ń': (color_blue, ' '),
             'ż': (color_black, ' '),
             'drzwi': (color_red, ' '),
             '': (color_yellow, ' '),
             'Θ': (color_character, 'Θ'),
             ' ': (color_normal, ' '),
             '┼': (color_doors, '┼')}
    for hor in range(len(board)):
        for ver in range(len(board[hor])):
            if board[hor][ver] not in paint:
                print(board[hor][ver], end='')
            else:
                print(paint[board[hor][ver]][0] + paint[board[hor][ver]][1] + color_normal, end='')
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


def print_inventory(inventory):
    '''Takes your inventory and displays it in a well-organized table with
    each column right-justified.'''
    items_number = 0
    for key in inventory:
        items_number += inventory[key]
    max_key_length = max(map(len, inventory))
    inventory_sorted = sorted(inventory.items(), key=operator.itemgetter(1), reverse=True)
    # Sorting(copying) of dict, changing it to list of tuples.
    print('Inventory:')
    print('  count    \b', ' '*(max_key_length-9), '\bitem name')
    print('-' * (11 + max_key_length))
    for i in range(len(inventory_sorted)):
        print(' ' * (6-len(str(inventory_sorted[i][1]))), inventory_sorted[i][1], ' ',
              ' ' * (max_key_length - len(inventory_sorted[i][0])), inventory_sorted[i][0])
    print('-' * (11 + max_key_length))
    print('Bag weight:', items_number, '\b/20 (bag size)')
    print('-' * (11 + max_key_length))
    print('Press P to exit')
    print('-' * (11 + max_key_length))


def player_move(key_input, x, y, board):
    """reads command from keybords and interact with game"""
    obstacles = ['ź', 'ł', 'ń', 'ż', 'ó']
    broadcast = None
    board[y][x] = ''
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
    if board[y][x] == '┼':
        broadcast = "doors"
    return x, y, broadcast


def main():
    os.system('clear')

    '''Introduction screen.'''
    while True:
        os.system('clear')
        print_board(create_board("intro.csv"))
        key_input = getch()
        break

    '''Menu screen.'''
    while True:
        os.system('clear')
        print_board(create_board("menu.csv"))
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

    questions_list = [['2 + 2 = ', '4'],
                      ['2 + 2 * 2 = ', '6'],
                      ['arka gdynia? ', 'kurwa świnia']]

    '''First stage. '''
    os.system('clear')
    player_interactions = [2, 2]  # starting position # list with factors depending on game progress
    board_change = "board1.csv"
    inventory = {'gówna': 1, 'patyki': 6}
    board = create_board(board_change)

    while True:
        interactions_on_board = insert_player(board, player_interactions[0], player_interactions[1])
        print_board(interactions_on_board)
        print_inventory(inventory)

        print(player_interactions)     # testowo

        key_input = getch()
        player_interactions = player_move(key_input, player_interactions[0], player_interactions[1], board)

        if player_interactions[2] is None:
            board_change = "board1.csv"   # do napsania funkcja zmieniająca plansze.

        elif player_interactions[2] is "change":
            board_change = "menu.csv"

        elif player_interactions[2] is 'doors':
            questions_no = random.choice(range(len(questions_list)))
            question = input(questions_list[questions_no][0])
            while question != questions_list[questions_no][1]:
                question = input(questions_list[questions_no][0])
            os.system('clear')

        elif player_interactions[2] is 'most1':
            pass

        elif player_interactions[2] is 'budynek1':
            pass

        os.system('clear')

    # '''Win screen.'''
    # while True:
    #     os.system('clear')
    #     print_board(create_board("win.csv"))
    #     key_input = getch()
    #     break
    #
    # '''Lose screen.'''
    # while True:
    #     os.system('clear')
    #     print_board(create_board("lose.csv"))
    #     key_input = getch()
    #     break

    '''Highscore.'''
    while True:
        os.system('clear')
        print_board(create_board("highscore.csv"))
        key_input = getch()
        break

if __name__ == '__main__':
    main()
