import csv

def import_inventory(filename="game_default_inventory.csv"):
    """import inventory from .csv file and merge it by name. Return new inventory"""
    dictionary = {}
    with open(filename, "r", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file, delimiter="|")
        for row in reader:
            dictionary[row[0]] = (row[1], row[2])
    return dictionary

def add_to_dictionary():
    """adding user input - name and two values to  dictionary"""
    dictionary = {}
    name_of_item = (input("Type a name of item:\n")).upper()
    first_value = (input("Type first value of item:\n")).upper()

    second_value = input("Type second value:\n")
    dictionary[name_of_item] = (first_value, second_value)
    return dictionary


def add_to_csv_inventory(inventory, filename="game_default_inventory.csv"):
    """write inventory to csv file with name comes as second argumment"""
    with open(filename, 'a', encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file, delimiter="|")
        for item in inventory:  # inventory is dictionary with two values
            writer.writerow((item, inventory[item][0], inventory[item][1]))
