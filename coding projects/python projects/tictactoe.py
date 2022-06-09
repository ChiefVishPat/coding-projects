import random
from tracemalloc import start

board = [ ['-', '-', '-'],
          ['-', '-', '-'],
          ['-', '-', '-'] ]

user = True #when user is true it refers to x, otherwise o
turns = 0

def print_board():
    for row in board:
        for col in row:
            print(f"{col} ", end="")
        print()

def quit(user_input):
    if(user_input == 'q'):
        print("Thanks for playing!")
        return True
    else: return False

def is_num(user_input):
    if not user_input.isnumeric():
        print("INVALID! Please enter a valid number")
        return False
    else: return True


def check_input(user_input):
    #check if input is a number
    if not is_num(user_input): return False
    user_input = int(user_input)

    #check if it is a number 1-9
    if user_input < 1 or user_input > 9:
        print('INVALID! Please enter a number 1 through 9')
        return False
    else: return True

def coordinates(user_input):
    row = int(user_input / 3)
    col = user_input
    if col > 2: col = int(col % 3)
    return (row,col)
    
def is_taken(coords, board):
    row = coords[0]
    col = coords[1]
    if board[row][col] != '-':
        print('This spot is already taken!')
        return True
    else: return False

def mark_board(coords, board, active_user) :
    row = coords[0]
    col = coords[1]
    board[row][col] = active_user


def current_user(user):
    if user: return 'x'
    else: return 'o'

def iswin(user, board):
    if check_row(user, board): return True
    if check_col(user, board): return True
    if check_diag(user, board): return True
    return False

def check_row(user, board):
    for row in board:
        complete_row = True
        for col in row:
            if col != user:
                complete_row = False
                break
        if complete_row: return True
    return False 

def check_col(user, board):
    for col in range(3):
        complete_col = True
        for row in range(3):
            if board[row][col] != user:
                complete_col = False
                break
        if complete_col: return True
    return False

def check_diag(user, board):
    #top left to bottom right
    if board[0][0] == user and board[1][1] == user and board[2][2] == user: return True
    elif board[0][2] == user and board[1][1] == user and board[2][0] == user: return True
    else: return False  

while turns < 9:
    active_user = current_user(user)
    print_board()
    user_input = input('Enter a number 1 to 9 or enter "q" to quit ')
    if quit(user_input): break
    if not check_input(user_input): continue
    user_input = int(user_input) - 1
    coords = coordinates(user_input)
    if is_taken(coords, board):
        print("Please try again")
        continue
    mark_board(coords, board, active_user)
    if iswin(active_user, board):
        print_board() 
        print(f"{active_user.upper()} won!")
        break

    turns += 1
    if turns == 9:
        print_board()
        print("Tie!")
    user = not user







#CREDIT: https://www.youtube.com/watch?v=n2o8ckO-lfk