import random

# Guess the Number game

range = input("Pick a range, 0 - MAX to guess from: ")
mystery_num = random.randint(0, int(range))
guesses = 0

while True:
    user_guess = int(input("Guess a number: "))
    guesses += 1

    if user_guess == mystery_num:
        print("You guessed it! The mystery number is:", mystery_num)
        break
    else:
        if user_guess < mystery_num:
            print("Guess higher!")
        else:
            print("Guess lower!")

print("You got it in", guesses, "tries")


