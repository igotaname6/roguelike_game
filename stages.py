import random
import os   # for screen clearing
import sys, tty, termios    # for getch() function
import datetime  # for time counting
import csv

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
            elif board[i][j] == '':
                print(' ', end='')
        print()


def insert_player(board, x, y):
    board[y][x] = (color_black + '@' + color_normal)
    return board


def main():
    create_board('board1.csv')
    insert_player(create_board(), 5, 5)

if __name__ == '__main__':
    main()
