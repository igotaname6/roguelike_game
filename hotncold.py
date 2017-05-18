import random

print('I am thinking of a 3-digit number. Try to guess what it is.\n\
      Here are some clues:\n\
      When I say:    That means:\n\
      Cold       No digit is correct.\n\
      Warm       One digit is correct but in the wrong position.\n\
      Hot        One digit is correct and in the right position.\n\
      I have thought up a number. You have 10 guesses to get it.')

random_digit = str(random.choice(range(100, 1000)))
# print(random_digit)

tries = 1
digit_input = input("Guess digit: ")
while digit_input != random_digit:
    print('Guess #', tries)
    if tries == 1:
        pass
    else:
        digit_input = input("Guess digit: ")

    list_random = [random_digit[0], random_digit[1], random_digit[2]]
    list_input = [digit_input[0], digit_input[1], digit_input[2]]
    index_of_hot = []
    count_hot = 0
    count_warm = 0
    count_cold = 0

    for i in range(len(list_input)):
        if list_input[i] == list_random[i]:
            count_hot += 1
            index_of_hot.append(i)

    list_to_check_warm = [0, 1, 2]
    for i in range(len(index_of_hot)):
        list_to_check_warm.remove(index_of_hot[i])

    for i in list_to_check_warm:
        if list_input[i] in list_random:
            count_warm += 1
        else:
            count_cold += 1
    if count_cold == 3:
        print("Cold")
    else:
        print("Hot " * count_hot, "Warm " * count_warm)

    tries += 1
print('You got it!')
