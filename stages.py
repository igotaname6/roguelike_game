import csv

color_building = '\033[3;37;47m'     # white - b
color_forest = '\033[3;32;42m'   # green - f
color_water = '\033[3;34;44m'    # blue - w
color_border = '\033[3;30;40m'   # black - x
color_normal = '\033[1;37;0m'     # 'normal'


def print_stage(filename='stage1.csv'):
    with open(filename, mode='r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        stage = []
        for row in reader:
            stage.append(row)

    for i in range(len(stage)):
        for j in range(len(stage[i])):
            if stage[i][j] == 'b':
                print(color_building + stage[i][j] + color_normal, end='')
            elif stage[i][j] == 'f':
                print(color_forest + stage[i][j] + color_normal, end='')
            elif stage[i][j] == 'w':
                print(color_water + stage[i][j] + color_normal, end='')
            elif stage[i][j] == 'x':
                print(color_border + stage[i][j] + color_normal, end='')
            elif stage[i][j] == '':
                print(' ', end='')
        print()


print_stage('stage1.csv')
