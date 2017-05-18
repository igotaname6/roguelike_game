import operator

def add_to_inventory(inventory, added_items):
    '''Adds to the inventory dictionary a list of items from added_items.'''
    for i in range(len(added_items)):
        if added_items[i] in inventory:
            inventory[added_items[i]] += 1
        else:
            inventory[added_items[i]] = 1


def print_inventory(inventory):
    '''Takes your inventory and displays it in a well-organized table with each column right-justified.'''
    items_weight = 0
    for key in inventory:
        items_weight += inventory[key][0] * inventory[key][1]
    max_key_length = max(map(len, inventory))
    inventory_sorted = sorted(inventory.items(), key=operator.itemgetter([1][0]), reverse=True)
    # Sorting(copying) of dict, changing it to list of tuples.
    print('|' + '-' * (20 + max_key_length) + '|')
    print('|     INVENTORY:', ' ' * max_key_length, '|')
    print('|' + '-' * (20 + max_key_length) + '|')
    print('| count | weight |', ' '*(max_key_length-11), 'item name |')
    print('|' + '-' * (20 + max_key_length) + '|')
    for i in range(len(inventory_sorted)):
        print('|', ' ' * (4 - len(str(inventory_sorted[i][1][0]))), inventory_sorted[i][1][0],
              '|', ' ' * (5 - len(str(inventory_sorted[i][1][1]))), inventory_sorted[i][1][1],
              '|', ' ' * (max_key_length - len(inventory_sorted[i][0])), inventory_sorted[i][0], '|')
    print('|' + '-' * (20 + max_key_length) + '|')
    print('|  ', 'Bag weight:', items_weight, '\b/20 kg  |')
    print('|' + '-' * (20 + max_key_length) + '|')


inventory = {'gówna': (1, 0.5), 'patyki': (6, 0.1)}
print_inventory(inventory)

'''
Player would like to gather at least 5 different items
(all items must have a name, a type and a weight) Types of items depends on the story of your game - i.e.
Clothes
Food
Weapons'''
