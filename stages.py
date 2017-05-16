from inventory_creator import import_inventory
import random
import os   # for screen clearing
import datetime  # for time counting
import csv
import sys, tty, termios    # for getch() function

color_white = '\033[3;37;47m'     # white _ character
color_char = '\033[1;31;47m'     # character
color_green = '\033[3;32;42m'   # green } forest
color_blue = '\033[3;34;44m'    # blue | water
color_black = '\033[3;30;40m'   # black ~ obstacles
color_brown = '\033[3;33;43m'   # brown ` doors, wood
color_normal = '\033[1;37;0m'     # 'normal'

obstacles = ['_', '}', '|', '~', '`']


def getch():    # WASD moving
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)  # wczytaj z systemu, z podstawowego wejscia, jeden znak
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def create_board(filename='board2.csv'):
    with open(filename, mode='r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        board = []
        for row in reader:
            board.append(row)
    return board    # return nested list [y][x]


def print_board(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == '_':
                print(color_white + board[i][j] + color_normal, end='')
            elif board[i][j] == '}':
                print(color_green + board[i][j] + color_normal, end='')
            elif board[i][j] == '|':
                print(color_blue + board[i][j] + color_normal, end='')
            elif board[i][j] == '~':
                print(color_black + board[i][j] + color_normal, end='')
            elif board[i][j] == 'Θ':
                print(color_char + board[i][j] + color_normal, end='')
            elif board[i][j] == '`':
                print(color_brown + board[i][j] + color_normal, end='')
            elif board[i][j] == '':
                print(' ', end='')
        print()
    print('Press P to exit')


def insert_player(board, x, y):
    board[y][x] = ('Θ')
    return board


def moving(key_input, x, y, board):
    if key_input == ("w"):
        y -= 1
        if board[y][x] in obstacles:
            y += 1
    elif key_input == ("a"):
        x -= 1
        if board[y][x] in obstacles:
            x += 1
    elif key_input == ("s"):
        y += 1
        if board[y][x] in obstacles:
            y -= 1
    elif key_input == ("d"):
        x += 1
        if board[y][x] in obstacles:
            x -= 1
    elif key_input == ("p"):
        exit()
    elif key_input == ("e"):
        pass
    return x, y

def menu_interactions(key_input):
    if key_input == "e":
        stage_change = 2
    return stage_change

def main():
    player_position = [15, 15]
    while True:
        print_board(insert_player(create_board(), player_position[0], player_position[1]))
        key_input = getch()
        player_position = moving(key_input, player_position[0], player_position[1], insert_player(create_board(),
                                 player_position[0], player_position[1]))
        os.system('clear')


if __name__ == '__main__':
    main()
