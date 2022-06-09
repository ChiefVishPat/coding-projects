import random

# create a list for the robot to choose from
choices_list = ["rock", "paper", "scissors"]

# score tracking variables
robot_score = 0
user_score = 0


def main():
    print("Welcome to rock, paper, scissors!")
    print("This game is best 2 out of 3")

    games_played = 0
    while games_played < 3:
        user = user_choice()
        robot = robot_choice()
        print("GAME:", games_played + 1)
        get_winner(user, robot)
        games_played += 1

    get_end_result()


# returns user choice
def user_choice():
    user = input('Choose either "rock", "paper", or "scissors": ')
    while user != "rock" and user != "paper" and user != "scissors":
        print('ERROR! Please input either "rock", "paper", or "scissors".')
        user = input('Choose either "rock", "paper", or "scissors": ')

    return user


# returns the robot choice
def robot_choice():
    robot = random.choice(choices_list)
    return robot


def get_winner(user, robot):
    global user_score, robot_score

    print("You chose:", user, "\nAnd the robot chose:", robot)
    if user == robot:
        print("tie!")
    elif (
        (user == "rock" and robot == "scissors")
        or (user == "scissors" and robot == "paper")
        or (user == "paper" and robot == "rock")
    ):
        user_score += 1
        print("You won this round")
    else:
        robot_score += 1
        print("you lost")


def get_end_result():
    if user_score > robot_score:
        print("You won the game! Congrats!")
    else:
        print("You lost :( \nBetter luck next time!")


main()

#forgot where but I used google for some help