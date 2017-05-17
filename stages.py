from inventory_creator import import_inventory
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
            elif board[horizon][vertical] == 'ó':
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
    print('Press P to exit')


def insert_player(board, x, y):
    """inserts avatar on the screen in game board"""
    board[y][x] = ('Θ')
    return board


def user_command(key_input, x, y, board):
    """reads command from keybords and interact with game"""
    obstacles = ['ź', 'ł', 'ń', 'ż', 'ó']
    if key_input == 'w':  # move avatr upward
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
    elif key_input == 'd':  # move riht
        x += 1
        if board[y][x] in obstacles:
            x -= 1
    elif key_input == 'p':  # exit from game
        exit()
    elif key_input == ("e"):  # show inventory
        brodcast = "change"
        return x, y, brodcast
    brodcast = None
    return x, y, brodcast

def main():
    '''Intro screen. '''
    print_board(create_board("intro.csv"))
    key_input = None
    while key_input != "x":
        key_input = getch()
        if key_input == 'p':
            exit()
    print_board(create_board('character_choose.csv'))
    key_input = None
    while key_input not in ["t", "n", "p"]:
        key_input = getch()
        #if key_input == 't':    # for terrorist
            #break
        #elif key_input == 'n':      # for navy
            #break
        if key_input == 'p':
            exit()

    '''First stage. '''
    game_factors = [2, 2]  # list with factors depending on game progress
    board_change = "board3.csv"
    while True:
        interactions_on_board = insert_player(create_board(board_change), game_factors[0], game_factors[1])
        print_board(interactions_on_board)
        key_input = getch()
        game_factors = user_command(key_input, game_factors[0], game_factors[1], interactions_on_board)
        if game_factors[2] is None:
            board_change = "board3.csv"   ### do napsania funkcja zmieniająca plansze.
        elif game_factors[2] is "change":
            board_change = "menu.csv"
        os.system('clear')


if __name__ == '__main__':
    main()
