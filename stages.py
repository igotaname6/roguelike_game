
import random
import os   # for screen clearing
import datetime  # for time counting
import csv
import sys, tty, termios    # for getch() function

color_white = '\033[3;37;47m'     # white - b
color_green = '\033[3;32;42m'   # green - f
color_blue = '\033[3;34;44m'    # blue - w
color_black = '\033[3;30;40m'   # black - x
color_normal = '\033[1;37;0m'     # 'normal'


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
            if board[i][j] == 'b':
                print(color_white + board[i][j] + color_normal, end='')
            elif board[i][j] == 'f':
                print(color_green + board[i][j] + color_normal, end='')
            elif board[i][j] == 'w':
                print(color_blue + board[i][j] + color_normal, end='')
            elif board[i][j] == 'x':
                print(color_black + board[i][j] + color_normal, end='')
            elif board[i][j] == '@':
                print(color_white + board[i][j] + color_normal, end='')
            elif board[i][j] == '':
                print(' ', end='')
        print()
    print('Press P to exit')


def insert_player(board, x, y):
    board[y][x] = ('@')
    return board


def moving(key_input, x, y):
    if key_input == ("w"):
        y -= 1
    elif key_input == ("a"):
        x -= 1
    elif key_input == ("s"):
        y += 1
    elif key_input == ("d"):
        x += 1
    elif key_input == ("p"):
        os.system('clear')
        exit()
    return x, y


def main():
    player_position = [15, 15]

    while True:
        print_board(insert_player(create_board(), player_position[0], player_position[1]))
        key_input = getch()
        player_position = moving(key_input, player_position[0], player_position[1])
        os.system('clear')


if __name__ == '__main__':
    main()
