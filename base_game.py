import math
import random

# Defines
LETTER_X = 1
LETTER_O = 2
EMPTY = 0

# Depending on who wins : LETTER_X / LETTER_O
TIE = 3
NOT_ENDED = 0

# 1 2 3
# 4 5 6
# 7 8 9

board_counter = 0  # Counts how many spaces are occupied
board = [  # 0 ha üres,1 ha X, 2 ha O
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]]


def clear_board():
    global board_counter
    for i in range(0, 3):
        for j in range(0, 3):
            board[i][j] = EMPTY
    board_counter = 0


def decode_pos(pos):  # Input: 1-9 numbers, Output: row, col; If invalid input, None is returned
    k = 1
    for i in range(0, 3):
        for j in range(0, 3):
            if pos == k:
                return i, j
            k += 1


def encode_pos(row, col):
    k = 1
    for i in range(0, 3):
        for j in range(0, 3):
            if i == row and j == col:
                return k
            k += 1


def put(pos, letter):  # Returns: -1, if not empty; 0, if no space; 1, if successful
    global board_counter

    row, col = decode_pos(pos)
    if board[row][col] != EMPTY:
        return -1
    if board_counter == 9:
        return 0
    board[row][col] = letter
    #  Ide majd a grafikus meghivást
    board_counter += 1
    return 1


def check_win():  # Returns NOT_ENDED,None; TIE,None; or WINNER,WIN_LIST; where WIN_LIST contains 3 positions
    if board_counter < 3:
        return NOT_ENDED, None

    win_list = []

    for i in range(0, 3):  # Looking by rows
        first = board[i][0]
        if first == board[i][1] and first == board[i][2]:
            win_list.append(encode_pos(i, 0))
            win_list.append(encode_pos(i, 1))
            win_list.append(encode_pos(i, 2))
            return first, win_list  # Winner

    for i in range(0, 3):  # Looking by columns
        first = board[0][i]
        if first == board[1][i] and first == board[2][i]:
            win_list.append(encode_pos(0, i))
            win_list.append(encode_pos(1, i))
            win_list.append(encode_pos(2, i))
            return first, win_list  # Winner

    first = board[0][0]
    if first == board[1][1] and first == board[2][2]:
        win_list.append(encode_pos(0, 0))
        win_list.append(encode_pos(1, 1))
        win_list.append(encode_pos(2, 2))
        return first, win_list

    first = board[0][2]
    if first == board[1][1] and first == board[2][0]:
        win_list.append(encode_pos(0, 2))
        win_list.append(encode_pos(1, 1))
        win_list.append(encode_pos(2, 0))
        return first, win_list

    if board_counter == 9:
        return TIE, None

    return NOT_ENDED, None


def decode_letter(letter):
    if letter == LETTER_O:
        return 'O'
    if letter == LETTER_X:
        return 'X'
    return ' '


def switch_player(letter):
    if letter == LETTER_O:
        return LETTER_X
    return LETTER_O


def print_board():
    for row in board:
        print('',end='| ')
        for col in row:
            print(decode_letter(col), end=' | ')
        print('\n-------------')


def start_game():
    clear_board()

    current_player = random.randint(1, 2)
    print(f'Starting player is {decode_letter(current_player)}')

    res, _ = check_win()
    while res == NOT_ENDED:
        # Putting on random pos
        random_pos = random.randint(1, 9)
        while put(random_pos, current_player) != 1:
            random_pos = random.randint(1, 9)
        res, win_list = check_win()
        # print_board()
        # print('\n')

        if res == NOT_ENDED:  # The game is not ended
            current_player = switch_player(current_player)
            continue

        if res == TIE:  # If the game is TIE
            print('The game finished TIE')
            print_board()
            return

        # When we have a winner

        print(f'The winner is: {decode_letter(current_player)}\n')
        print_board()
        print(f'The win list: {win_list}')
        return


start_game()