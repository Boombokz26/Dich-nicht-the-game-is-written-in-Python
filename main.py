import random


# calculate size of the board using its structure
def calculate_size(board):
    return (len(board[0]) + 4) // 4


# calculate size of the board list
def board_size(n):
    return n * 4 - 4


# calculate size of the home path
def home_size(n):
    return n // 2 - 1


# generate the board
####################
# the board is just a list of characters, each of which will be
# printed out to the screen
# the list starts at the position of first player's begin
# position and goes around the field, simulating the first
# player's path
#
# this function returns a tuple, that tuple contains:
# [0] = board
# [1] = home path of the first player
# [2] = home path of the second player
def gensachovnicu(n):
    if n % 2 == 0:
        return None
    return ['*' for i in range(board_size(n))], ['D' for i in range(home_size(n))], \
           ['D' for i in range(home_size(n))]


# print given board
####################
# I am printing this board by dividing it to sections:
# - top row, 3 elements
# - top rows between the middle cross-section and the top row, 3 elements as well
# - 3 rows of the middle cross-section, each n elements
# - bottom rows between the middle cross-section and the bottom row, 3 elements
# - bottom row, 3 elements
#
# each character takes 3 horizontal places, so they are padded using spaces
def tlacsachovnicu(input_board):
    n = calculate_size(input_board)
    output = []  # a list of strings that will be printed out
    board = input_board[0]
    home_x = input_board[1]
    home_y = input_board[2]

    x = 0  # next printed character from the right part
    y = -1  # next printed character from the left part

    x_h = 0  # next printed top home character
    y_h = -1  # next printed bottom home character
    for i in range(n + 1):
        if i == 0:
            output.append("   ")
            for j in range(n):
                output[0] += "{:3d}".format(j)
            continue
        output.append("{:3d}".format(i - 1))
        if i - 1 == 0:  # first row
            # insert blank spaces before the column
            for j in range(n // 2 - 1):
                output[i] += "   "

            # this line uses slices to get two elements from the end and one from the beginning
            for character in board[-2:] + board[:1]:
                output[i] += "  " + character
            x += 1
            y -= 2

            # insert blank spaces after the column
            for j in range(n // 2 - 1):
                output[i] += "   "
        elif (n - 1) // 2 - 1 > i - 1:  # section that goes after the 1 row, but before the middle section
            # insert blank spaces before the column
            for j in range(n // 2 - 1):
                output[i] += "   "

            # take the element from the end and from the beginning
            output[i] += "  " + board[y] + "  " + home_x[x_h] + "  " + board[x]
            x_h += 1
            x += 1
            y -= 1

            # insert blank spaces after the column
            for j in range(n // 2 - 1):
                output[i] += "   "
        elif (n - 1) // 2 - 1 == i - 1:  # 1 row of middle section
            # print the left part
            temp = []
            for j in range(n // 2):
                temp.append("  " + board[y])
                y -= 1
            for j in temp[::-1]:
                output[i] += j
            # print the middle
            output[i] += "  " + home_x[x_h]
            x_h += 1

            # print the right part
            for j in range(n // 2):
                output[i] += "  " + board[x]
                x += 1
        elif (n - 1) // 2 == i - 1:  # 2 row of middle section
            output[i] += "  " + board[y]
            y -= 1
            for j in range((n - 2) // 2):
                output[i] += "  D"
            output[i] += "  X"
            for j in range((n - 2) // 2):
                output[i] += "  D"
            output[i] += "  " + board[x]
            x += 1
        elif (n - 1) // 2 + 1 == i - 1:  # 3 row of middle section
            for j in range(n // 2):
                output[i] += "  " + board[y]
                y -= 1
            output[i] += "  " + home_y[y_h]
            y_h -= 1
            temp = []
            for j in range(n // 2):
                temp.append("  " + board[x])
                x += 1
            for j in temp[::-1]:
                output[i] += j
        elif n - 1 > i - 1:  # section after the middle section
            # insert blank spaces before the column
            for j in range(n // 2 - 1):
                output[i] += "   "

            # take the element from the end and from the beginning
            output[i] += "  " + board[y] + \
                         "  " + home_y[y_h] + \
                         "  " + board[x]
            y_h -= 1
            x += 1
            y -= 1

            # insert blank spaces after the column
            for j in range(n // 2 - 1):
                output[i] += "   "
        elif n - 1 == i - 1:  # last row
            # insert blank spaces before the column
            for j in range(n // 2 - 1):
                output[i] += "   "

            for j in range(3):
                output[i] += "  " + board[y]
                y -= 1

            # insert blank spaces after the column
            for j in range(n // 2 - 1):
                output[i] += "   "
    for i in output:
        print(i)


# returns the initial position of the second player
def get_second_position(n):
    return (n // 2) * 4


# transforms the relative coordinate of the second player
# to absolute position on the board
def to_second(x, n):
    return (x + get_second_position(n)) % board_size(n)


# a function to make 1 step
# the function accepts a board, position of the first player,
# and optionally position of the second player
#
# returns the resulting board, position of the first player,
# position of the second player, score that the first player
# gained on that step and the second player's score
def simulate_step(board, first_pos, second_pos=-1):
    n = calculate_size(board)
    dice = random.randint(1, 6)
    first_score = 0
    second_score = 0

    print("First dice:", dice)
    if first_pos < board_size(n):
        # the player is going around the board
        board[0][first_pos] = '*'
        if first_pos + dice < board_size(n):
            # the player will be still on the board
            first_pos += dice
            board[0][first_pos] = 'A'
            if first_pos == to_second(second_pos, n):
                second_pos = 0
                board[0][to_second(second_pos, n)] = 'B'
                if to_second(second_pos, n) == first_pos:
                    # if the first player caught the second on its spawn, reset them both
                    first_pos = 0
                    board[0][first_pos] = 'A'
        else:
            # the player goes on the home line
            if (first_pos + dice) % board_size(n) < home_size(n):
                # the player will go on the home path
                board[1][(first_pos + dice) % board_size(n)] = 'A'
                first_pos += dice
            else:
                # the player skips the home path and goes to the target
                first_pos = 0
                board[0][first_pos] = 'A'
                first_score += 1
    else:
        # the player is running home
        home_pos = first_pos % board_size(n)
        board[1][home_pos] = 'D'
        if home_pos + dice < home_size(n):
            # the player will still be on the way home
            board[1][home_pos + dice] = 'A'
            first_pos += dice
        else:
            # the player score 1 point and goes back
            first_score += 1
            board[0][0] = 'A'
            first_pos = 0

    if second_pos < 0:
        return board, first_pos, second_pos, first_score, second_score

    dice = random.randint(1, 6)
    print("Second dice:", dice)
    if second_pos < board_size(n):
        # the player is going around the board
        board[0][to_second(second_pos, n)] = '*'
        if second_pos + dice < board_size(n):
            # the player will be still on the board
            second_pos += dice
            board[0][to_second(second_pos, n)] = 'B'
            if first_pos == to_second(second_pos, n):
                first_pos = 0
                board[0][first_pos] = 'A'
                if first_pos == to_second(second_pos, n):
                    # the second player caught the first player on its spawn, reset them both
                    second_pos = 0
                    board[0][(second_pos + get_second_position(n)) % board_size(n)] = 'B'
        else:
            # the player goes on the home line
            if (second_pos + dice) % board_size(n) < home_size(n):
                # the player will go on the home path
                board[2][(second_pos + dice) % board_size(n)] = 'B'
                second_pos += dice
            else:
                # skip the home path
                second_pos = 0
                board[0][to_second(second_pos, n)] = 'B'
                second_score += 1
    else:
        # the player is running home
        home_pos = second_pos % board_size(n)
        board[2][home_pos] = 'D'
        if home_pos + dice < home_size(n):
            # the player will still be on the way home
            board[2][home_pos + dice] = 'B'
            second_pos += dice
        else:
            # the player score 1 point and goes back
            second_score += 1
            second_pos = 0
            board[0][to_second(second_pos, n)] = 'B'

    return board, first_pos, second_pos, first_score, second_score


def main():
    n = input("Please, input the board size (default = 9, min = 5): ")
    if len(n) == 0:
        n = 9
    else:
        n = int(n)
    while n % 2 == 0 or n < 5:
        n = input("Please, specify an odd number (default = 9, min = 5): ")
        if len(n) == 0:
            n = 9
        else:
            n = int(n)
    print("Generating the board...")
    board = gensachovnicu(n)
    print("===========================================")
    needed_score = (n - 3) // 2
    first_pos = 0
    first_score = 0
    second_pos = 0
    second_score = 0
    while first_score != needed_score and second_score != needed_score:
        print("Making a turn...")
        temp = simulate_step(board, first_pos, second_pos)

        board = temp[0]
        first_pos = temp[1]
        second_pos = temp[2]
        first_score += temp[3]
        second_score += temp[4]

        tlacsachovnicu(board)
        print("First player's score:", first_score)
        print("Second player's score:", second_score)
        print("===========================================")


if __name__ == '__main__':
    main()
