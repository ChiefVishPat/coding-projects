board = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7],
]

# prints the sudoku board in a visually pleasing format :)
def print_board(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - -")

        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")


# attempts to find an empty spot on the board
# if an empty spot is found, it returns (row,col)
# if no empty spots are found, the method returns None
def find_empty(board):
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == 0:
                return (row, col)
    return None


# checks each row, column, and square for duplicate numbers
# if a duplicate is found, False is returned, otherwise True is returned
def valid(board, position, num):
    # check row
    for i in range(len(board[0])):
        # essentially this checks to see if the num we inserted in is equal to any of the spaces
        # as long as it is not equal to the position of the cell we inserted the num into
        if board[position[0]][i] == num and position[1] != i:
            return False

    # check col
    # same logic as above
    for i in range(len(board)):
        if board[i][position[1]] == num and position[0] != i:
            return False

    # calculates the square we should be in
    square_row = position[0] // 3  # i.e the y coord
    square_col = position[1] // 3  # i.e the x coord

    # check square:
    # finds the right square we are in.
    # once found, we check the number on the board to see if its equal to the num
    # we inserted and make sure the num coord is not the same as the position coords
    for row in range(square_row*3, square_row*3 + 3):
        for col in range(square_col*3, square_col*3 + 3):
            if board[row][col] == num and (row, col) != position:
                return False

    return True


def solve(board):
    find = find_empty(board)
    if not find:
        return True
    else:
        row, col = find

    # try each possible number in each cell
    for i in range(1, 10):
        if valid(board, (row, col), i):  # finds a valid spot on the board to insert a number inserts
            board[row][col] = i          # the valid number into the board if the spot is valid

            if solve(board):    # we call solve() on the new board with the number we just added
                return True     # returns true if we filled the board correctly

            # if solve() returns false, that means the values we tried out did not work
            # This means we backtrack and the previous number is reset to 0
            board[row][col] = 0

    return False  # no possible solutions found


print_board(board)
solve(board)
print("\n\n")
print_board(board)


#credit: https://www.techwithtim.net/tutorials/python-programming/sudoku-solver-backtracking/
