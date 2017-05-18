
def go_through_doors(entry, doors_state, exit):
    if doors_state == 'inside':
        game_factors = [entry[0], entry[1]]
        doors_state = 'outside'
    else:
        game_factors = [exit[0], exit[1]]
        doors_state = 'inside'
    os.system('clear')
    return doors_state, game_factors


print(go_through_doors([3, 5], doors_state, [3, 7]))
