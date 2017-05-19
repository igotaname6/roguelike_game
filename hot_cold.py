import random
import time


def user_input(n):
    correct_number = None
    while correct_number is None:
        try:
            number = int(input("Its your {} attempt,type a three-digit number: ".format(n)))
            if number > 999 or number < 100:
                raise ValueError
            correct_number = number
        except ValueError:
            print("This is no number or it don't have 3 digits")
    return list(str(correct_number))


def create_number():
    while True:
        random_number = list(str(random.randint(100, 999)))
        if random_number[0] == random_number[1] \
            or random_number[1] == random_number[2] \
                or random_number[2] == random_number[0]:
            pass
        else:
            break
    return random_number


def set_difficulty():
    while True:
        user_choise = input("Choose difficulty level")
        if user_choise in ["5", "10", "15"]:
            break
    return int(user_choise)


# print("""I am thinking of a 3-digit number. Try to guess what it is.
#
# Here are some clues:
#
# When I say:    That means:
#
#   Cold       No digit is correct.
#
#   Warm       One digit is correct but in the wrong position.
#
#   Hot        One digit is correct and in the right position.
#
# I have thought up a number. You have 10 guesses to get it.) """)

def game():
    number_to_guess_original = create_number()
    print(number_to_guess_original)
    n = 1
    start = time.time()
    difficulty = 30
    while n <= difficulty:
        cold_check = 0
        number_to_guess = number_to_guess_original[:]
        user_guess = user_input(n)
        if user_guess == number_to_guess:
            print("You won!")
            end = time.time()
            print("{:.3}".format(end-start))
            return "win"
        else:
            i = 0
            while i < len(number_to_guess):
                if number_to_guess[i] == user_guess[i]:
                    print("Hot")
                    number_to_guess.pop(i)
                    user_guess.pop(i)
                else:
                    i += 1
        for digit in user_guess:
            if digit in number_to_guess:
                print("warm")
            else:
                cold_check += 1
        if cold_check == 3:
            print("Cold")
        n += 1
