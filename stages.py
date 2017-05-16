
import random
import os   # for screen clearing
import datetime  # for time counting
import csv
import sys, tty, termios    # for getch() function


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

obstacles = ['ź', 'ł', 'ń', 'ż']


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
    with open(filename, mode='r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        board = []
        for row in reader:
            board.append(row)
    return board    # return nested list [y][x]


def print_board(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 'ź':
                print(color_white + ' ' + color_normal, end='')
            elif board[i][j] == 'ł':
                print(color_green + ' ' + color_normal, end='')
            elif board[i][j] == 'ń':
                print(color_blue + ' ' + color_normal, end='')
            elif board[i][j] == 'ż':
                print(color_black + ' ' + color_normal, end='')
            elif board[i][j] == 'drzwi':
                print(color_red + ' ' + color_normal, end='')
            elif board[i][j] == 'Θ':
                print(color_character + board[i][j] + color_normal, end='')
            elif board[i][j] == '':
                print(color_yellow + ' ' + color_normal, end='')
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
    return x, y


def main():
    player_position = [2, 2]
    while True:
        print_board(insert_player(create_board(), player_position[0], player_position[1]))
        key_input = getch()
        player_position = moving(key_input, player_position[0], player_position[1], insert_player(create_board(),
                                 player_position[0], player_position[1]))
        os.system('clear')


if __name__ == '__main__':
    main()
