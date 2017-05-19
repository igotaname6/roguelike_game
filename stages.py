import hot_cold
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
color_purple = '\033[1;30;43m'
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
    for i in range(15):
        x = random.choice(range(0, 30))
        y = random.choice(range(0, 100))
        if board[x][y] == '':
            board[x][y] = '∞'
    for i in range(15):
        x = random.choice(range(0, 30))
        y = random.choice(range(0, 100))
        if board[x][y] == '':
            board[x][y] = '└'
    for i in range(15):
        x = random.choice(range(0, 30))
        y = random.choice(range(0, 100))
        if board[x][y] == '':
            board[x][y] = '$'
    for i in range(5):
        x = random.choice(range(0, 30))
        y = random.choice(range(0, 100))
        if board[x][y] == '':
            board[x][y] = '§'
    for i in range(5):
        x = random.choice(range(0, 30))
        y = random.choice(range(0, 100))
        if board[x][y] == '':
            board[x][y] = '/'
    return board    # return nested list [y][x]


def print_board(board):
    """Prints board on the screen and colouring by characters"""
    paint = {'ź': (color_white, ' '),
             'ł': (color_green, ' '),
             'ń': (color_blue, ' '),
             'ż': (color_black, ' '),
             '': (color_yellow, ' '),
             'Θ': (color_character, 'Θ'),
             ' ': (color_normal, ' '),
             'ó': (color_red, ' '),
             '┼': (color_doors, '┼'),
             '∞': (color_purple, '∞'),
             '└': (color_purple, '└'),
             '$': (color_purple, '$'),
             '§': (color_purple, '§'),
             '/': (color_purple, '/')}
    for hor in range(len(board)):
        for ver in range(len(board[hor])):
            if board[hor][ver] not in paint:
                print(board[hor][ver], end='')
            else:
                print(paint[board[hor][ver]][0] + paint[board[hor][ver]][1] + color_normal, end='')
        print()


def insert_player(board, x=0, y=0):
    """inserts avatar on the screen in game board"""
    board[y][x] = ('Θ')
    return board


def add_to_inventory(inventory, added_items):
    '''Adds to the inventory dictionary a list of items from added_items.'''
    if added_items[0] in inventory:
        inventory[added_items[0]][0] += 1
    else:
        inventory[added_items[0]] = [added_items[1], added_items[2]]


def print_inventory(inventory):
    '''Takes your inventory and displays it in a well-organized table with each column right-justified.'''
    items_weight = 0
    for key in inventory:
        items_weight += inventory[key][0] * inventory[key][1]
    max_key_length = max(map(len, inventory))
    inventory_sorted = sorted(inventory.items(), key=operator.itemgetter([1][0]), reverse=True)
    # Sorting(copying) of dict, changing it to list of tuples.
    print('|' + '-' * (20 + max_key_length) + '|')
    print('|        INVENTORY:', ' ' * max_key_length, '|')
    print('|' + '-' * (20 + max_key_length) + '|')
    print('| count | weight | item name |')
    print('|' + '-' * (20 + max_key_length) + '|')
    for i in range(len(inventory_sorted)):
        print('|', ' ' * (4 - len(str(inventory_sorted[i][1][0]))), inventory_sorted[i][1][0],
              '|', ' ' * (5 - len(str(inventory_sorted[i][1][1]))), inventory_sorted[i][1][1],
              '|', ' ' * (max_key_length - len(inventory_sorted[i][0])), inventory_sorted[i][0], '|')
    print('|' + '-' * (20 + max_key_length) + '|')
    print('|  ', 'Bag weight:', round(items_weight, 2), '\b/20 kg   |')
    print('|' + '-' * (20 + max_key_length) + '|')


def make_it_short(word, length):
    '''HIGHSCORE - Make length of the word equal to chosen length and returns it'''
    if len(str(word)) <= length:
        word = (length - len(str(word))) * " " + str(word)
        return str(word)
    elif len(str(word)) > length:
        word = str(word)[0:length]
        return str(word)


def print_highscore(time_start, time_end, player_name, items_collected, board_width=100, board_height=30):  # board with size
    '''Highscore'''
    gamedate = datetime.date.today()  # date of game
    player_time = (time_end - time_start).seconds  # how long did player play
    points = int((int(items_collected) ** 4) / int(player_time)) * 100
    players_score = [make_it_short(i, 13) for i in [player_name, gamedate, items_collected, player_time, points]]
    with open('highscores.txt', 'a') as highscore_add:  # opens and adds result to highscore
        highscore_add.write(" | ".join(players_score) + "\n")

    # HIGHSCORE SORT
    highscore = []
    with open('highscores.txt', 'r') as read:  # opens highscores.txt in read mode
        for i in range(sum(1 for line in open('highscores.txt'))):
            highscore.append(read.readline().split("|"))    # rozjebujemy liste zeby dostac sie do punktow
    highscore = sorted(highscore, key=lambda y: y[int(4)])    # sortujemy wg punktow
    highscore.reverse()
    for i in range(len(highscore)):
        highscore[i] = ("|".join(highscore[i]))

    board_list = []
    board_list.append(list("ż") * board_width)
    board_list.append("ż                                           So far highscores:                                                X")
    board_list.append("ż Soldier name|     Date      |Items collected|      Time     |    Points     ż")
    board_list.append(highscore)
    board_list.append(board_list[0])
    board_list.append('PRESS ANY KEY TO EXIT')
    return board_list


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
    if board[y][x] == '┼':
        broadcast = "doors"
    if board[y][x] == '∞':
        broadcast = 'dynamite'
    if board[y][x] == '└':
        broadcast = 'ammo'
    if board[y][x] == '$':
        broadcast = 'coins'
    if board[y][x] == '§':
        broadcast = 'rope'
    if board[y][x] == '/':
        broadcast = 'pistol'
    if [x, y] == [94, 31]:
        broadcast = 'next_lvl'
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
            # print_board(print_highscore(time_start, time_end, player_name, items_collected))
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

    items_collected = 0
    questions_list = [['2 + 2 = ', '4'],
                      ['2 + 2 * 2 = ', '6'],
                      ['"Sneaky" programming language? ', 'python'],
                      ['2 ^ 3 = ', '8']]
    inventory = {'dynamite': [1, 0.5], 'ammo': [1, 0.1], 'coin': [1, 0.05]}   # poczatkowy inwentarz

    '''First stage. '''
    os.system('clear')
    time_start = datetime.datetime.today()  # set stopwatch on
    player_interactions = [2, 2]  # starting position
    board_change = "board1.csv"
    board = create_board(board_change)
    interactions_on_board = insert_player(board, player_interactions[0], player_interactions[1])
    print_board(interactions_on_board)
    print_inventory(inventory)
    player_name = input('Enter your name: ')

    while True:
        '''First stage.'''
        os.system('clear')
        interactions_on_board = insert_player(board, player_interactions[0], player_interactions[1])
        print_board(interactions_on_board)
        print_inventory(inventory)
        print(player_interactions)     # testowo
        key_input = getch()
        player_interactions = player_move(key_input, player_interactions[0], player_interactions[1], board)

        if player_interactions[2] is 'doors':
            questions_no = random.choice(range(len(questions_list)))
            question = input(questions_list[questions_no][0])
            while question != questions_list[questions_no][1]:
                question = input(questions_list[questions_no][0])
        elif player_interactions[2] is 'dynamite':
            dragon_loot = ['dynamite', 1, 0.5]
            add_to_inventory(inventory, dragon_loot)
            items_collected += 1
        elif player_interactions[2] is 'ammo':
            dragon_loot = ['ammo', 1, 0.1]
            add_to_inventory(inventory, dragon_loot)
            items_collected += 1
        elif player_interactions[2] is 'coins':
            dragon_loot = ['coin', 1, 0.05]
            add_to_inventory(inventory, dragon_loot)
            items_collected += 1
        elif player_interactions[2] is 'rope':
            dragon_loot = ['rope', 1, 2]
            add_to_inventory(inventory, dragon_loot)
            items_collected += 1
        elif player_interactions[2] is 'pistol':
            dragon_loot = ['pistol', 1, 1]
            add_to_inventory(inventory, dragon_loot)
            items_collected += 1
        elif player_interactions[2] is 'next_lvl':
            break
        os.system('clear')

    '''Second stage. '''
    os.system('clear')
    player_interactions = [93, 29]  # starting position
    board_change = "board2.csv"
    board = create_board(board_change)
    while True:
        interactions_on_board = insert_player(board, player_interactions[0], player_interactions[1])
        print_board(interactions_on_board)
        print_inventory(inventory)
        print(player_interactions)     # testowo
        key_input = getch()
        player_interactions = player_move(key_input, player_interactions[0], player_interactions[1], board)

        if player_interactions[2] is 'doors':
            questions_no = random.choice(range(len(questions_list)))
            question = input(questions_list[questions_no][0])
            while question != questions_list[questions_no][1]:
                question = input(questions_list[questions_no][0])
        elif player_interactions[2] is 'dynamite':
            dragon_loot = ['dynamite', 1, 0.5]
            add_to_inventory(inventory, dragon_loot)
            items_collected += 1
        elif player_interactions[2] is 'ammo':
            dragon_loot = ['ammo', 1, 0.1]
            add_to_inventory(inventory, dragon_loot)
            items_collected += 1
        elif player_interactions[2] is 'coins':
            dragon_loot = ['coin', 1, 0.05]
            add_to_inventory(inventory, dragon_loot)
            items_collected += 1
        elif player_interactions[2] is 'rope':
            dragon_loot = ['rope', 1, 2]
            add_to_inventory(inventory, dragon_loot)
            items_collected += 1
        elif player_interactions[2] is 'pistol':
            dragon_loot = ['pistol', 1, 1]
            add_to_inventory(inventory, dragon_loot)
            items_collected += 1
        elif player_interactions[2] is 'next_lvl':
            break
        os.system('clear')

    '''Third stage. '''
    os.system('clear')
    player_interactions = [2, 2]  # starting position
    board_change = "board3.csv"
    board = create_board(board_change)
    while True:
        interactions_on_board = insert_player(board, player_interactions[0], player_interactions[1])
        print_board(interactions_on_board)
        print_inventory(inventory)
        print(player_interactions)     # testowo
        key_input = getch()
        player_interactions = player_move(key_input, player_interactions[0], player_interactions[1], board)

        if player_interactions[2] is 'doors':
            questions_no = random.choice(range(len(questions_list)))
            question = input(questions_list[questions_no][0])
            while question != questions_list[questions_no][1]:
                question = input(questions_list[questions_no][0])
        elif player_interactions[2] is 'dynamite':
            dragon_loot = ['dynamite', 1, 0.5]
            add_to_inventory(inventory, dragon_loot)
            items_collected += 1
        elif player_interactions[2] is 'ammo':
            dragon_loot = ['ammo', 1, 0.1]
            add_to_inventory(inventory, dragon_loot)
            items_collected += 1
        elif player_interactions[2] is 'coins':
            dragon_loot = ['coin', 1, 0.05]
            add_to_inventory(inventory, dragon_loot)
            items_collected += 1
        elif player_interactions[2] is 'rope':
            dragon_loot = ['rope', 1, 2]
            add_to_inventory(inventory, dragon_loot)
            items_collected += 1
        elif player_interactions[2] is 'pistol':
            dragon_loot = ['pistol', 1, 1]
            add_to_inventory(inventory, dragon_loot)
            items_collected += 1
        elif player_interactions[2] is 'next_lvl':
            break
        os.system('clear')

    '''Fourth stage. '''
    os.system('clear')
    player_interactions = [2, 2]  # starting position
    board_change = "board4.csv"
    board = create_board(board_change)
    while True:
        interactions_on_board = insert_player(board, player_interactions[0], player_interactions[1])
        print_board(interactions_on_board)
        print_inventory(inventory)
        print(player_interactions)     # testowo
        key_input = getch()
        player_interactions = player_move(key_input, player_interactions[0], player_interactions[1], board)

        if player_interactions[2] is 'doors':
            questions_no = random.choice(range(len(questions_list)))
            question = input(questions_list[questions_no][0])
            while question != questions_list[questions_no][1]:
                question = input(questions_list[questions_no][0])
        elif player_interactions[2] is 'dynamite':
            dragon_loot = ['dynamite', 1, 0.5]
            add_to_inventory(inventory, dragon_loot)
            items_collected += 1
        elif player_interactions[2] is 'ammo':
            dragon_loot = ['ammo', 1, 0.1]
            add_to_inventory(inventory, dragon_loot)
            items_collected += 1
        elif player_interactions[2] is 'coins':
            dragon_loot = ['coin', 1, 0.05]
            add_to_inventory(inventory, dragon_loot)
            items_collected += 1
        elif player_interactions[2] is 'rope':
            dragon_loot = ['rope', 1, 2]
            add_to_inventory(inventory, dragon_loot)
            items_collected += 1
        elif player_interactions[2] is 'pistol':
            dragon_loot = ['pistol', 1, 1]
            add_to_inventory(inventory, dragon_loot)
            items_collected += 1
        elif player_interactions[2] is 'next_lvl':
            break
        os.system('clear')

    '''The Boss stage - hotncold game. '''
    os.system('clear')
    board_change = "boss.csv"
    board = create_board(board_change)
    key_input = getch()
    while True:
        interactions_on_board = insert_player(board)
        print_board(interactions_on_board)
        key_input = getch()
        os.system('clear')

        game_end = hot_cold.game()      # return string 'win'
        break
    time_end = datetime.datetime.today()  # set stopwatch off

    '''Win screen.'''
    while True:
        os.system('clear')
        print_board(create_board("win.csv"))
        key_input = getch()
        break

    # '''Lose screen.'''
    # while True:
    #     os.system('clear')
    #     print_board(create_board("lose.csv"))
    #     key_input = getch()
    #     break

    '''Highscore.'''
    while True:
        os.system('clear')
        print_board(print_highscore(time_start, time_end, player_name, items_collected))
        # print_board(create_board("highscore.csv"))
        key_input = getch()
        break


if __name__ == '__main__':
    main()
