import math
import random
import queue
import sys
import os
import time
import threading
import multiprocessing
import pages
from utils.error import sendError

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'UI'))

queue = queue.Queue()

# Defines
LETTER_X = 1
LETTER_O = 2
EMPTY = 0

GAME_PVP = 1
GAME_PVE = 2
GAME_SAMEPC = 3

PLAYER_ME = 1
PLAYER_PC = 0
PLAYER_P2 = 2

# Depending on who wins : LETTER_X / LETTER_O
TIE = 3
NOT_ENDED = 0

# 1 2 3
# 4 5 6
# 7 8 9

board_counter = 0  # Counts how many spaces are occupied
starting_player = 0  # 0 - Me/P1, 1 - PC/P2
current_player = 0  # Same as starting, X is always starting
game_type = 0
current_round = 0
sig = False
round_list = [-1, -1, -1, -1]
match_ended = False
roundend_event = threading.Event()
board = [  # 0 ha üres,1 ha X, 2 ha O
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]]


def clear_board(r=False):
    try:
        global board_counter, current_round
        for i in range(0, 3):
            if r:
                round_list[i] = -1
            for j in range(0, 3):
                board[i][j] = EMPTY
        board_counter = 0
        if r:
            current_round = 0
        if not queue.empty():
            queue.get()
    except Exception as e:
        sendError("Error in base_game.py/clear_board", str(e))


def decode_player(player):
    if player == PLAYER_PC:
        return 'PC'
    elif player == PLAYER_P2:
        return 'Player2'
    else:
        return 'Player1'


def decode_pos(pos):  # Input: 1-9 numbers, Output: row, col; If invalid input, exception raised
    try:
        k = 1
        for i in range(0, 3):
            for j in range(0, 3):
                if pos == k:
                    return i, j
                k += 1
        raise Exception("Pos was not found!")
    except Exception as e:
        sendError("Error in base_game.py/decode_pos", str(e))
        return None


def encode_pos(row, col):
    try:
        k = 1
        for i in range(0, 3):
            for j in range(0, 3):
                if i == row and j == col:
                    return k
                k += 1
        raise Exception("Pos was not found!")
    except Exception as e:
        sendError("Error in base_game.py/encode_pos", str(e))
        return None


def check_win():  # Returns NOT_ENDED,None; TIE,None; or WINNER,WIN_LIST; where WIN_LIST contains 3 positions
    try:
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
    except Exception as e:
        sendError("Error in base_game.py/check_win", str(e))


def decode_letter(letter):
    if letter == LETTER_O:
        return 'O'
    if letter == LETTER_X:
        return 'X'
    return ' '


def switch_letter(letter):
    if letter == LETTER_O:
        return LETTER_X
    return LETTER_O


def print_board():
    try:
        for row in board:
            print('', end='| ')
            for col in row:
                print(decode_letter(col), end=' | ')
            print('\n-------------')
        print('')
    except Exception as e:
        sendError("Error in base_game.py/print_board", str(e))


def exit_game_delayed():
    try:
        global match_ended
        match_ended = True
        clear_board(True)
    except Exception as e:
        sendError("Error in base_game.py/exit_game_delayed", str(e))


def switch_player(p):
    if game_type == GAME_PVE:
        if p == PLAYER_PC:
            return PLAYER_ME
        return PLAYER_PC
    if game_type == GAME_SAMEPC:
        if p == PLAYER_ME:
            return PLAYER_P2
        return PLAYER_ME
    return PLAYER_ME


def next_round(tie=False):
    try:
        global current_round, current_player, starting_player, match_ended, sig
        clear_board()
        if tie:
            print('Restarting this round...\n')
            sig = True
            current_player = starting_player = switch_player(starting_player)
            print(f'The starting player is {decode_player(current_player)}\n')
            if current_player == PLAYER_PC:
                threading.Thread(target=request_random_step).start()
            return
        elif current_round == 3:  # Game end
            p1_won = 0
            for i in round_list:
                if i == PLAYER_ME:
                    p1_won += 1
            if game_type == GAME_PVE:
                tmp = PLAYER_PC if p1_won <= 1 else PLAYER_ME
            elif game_type == GAME_SAMEPC:
                tmp = PLAYER_P2 if p1_won <= 1 else PLAYER_ME
            else:
                tmp = PLAYER_ME
            print(f'The winner of the match is {decode_player(tmp)}! Rounds won: {[decode_player(round_list[value]) for value in range(1, len(round_list)) if value != 0]}\n')
            threading.Timer(4, exit_game_delayed).start()
            return

        current_round += 1
        current_player = starting_player = switch_player(starting_player)
        if current_player == PLAYER_PC:
            threading.Thread(target=request_random_step).start()
        print(f'The starting player is: {decode_player(current_player)}\n')

        # TODO: Betolteni ujra a 6.os oldalt, megvaltoztatva a roundlistet [roundlist] szerint
    except Exception as e:
        sendError("Error in base_game.py/next_round", str(e))


def request_put(pos, player):  # A grafikus felulet ezt hivja meg
    try:
        global current_player
        if player == 3:
            player = PLAYER_ME if game_type == GAME_PVE else current_player
        if player != current_player:
            return 0

        res = put(pos, LETTER_X if starting_player == current_player else LETTER_O)
        win, _ = check_win()
        if game_type == GAME_PVE:
            if current_player == PLAYER_ME:
                if res == 1:  # Successful, so PC turn
                    current_player = switch_player(current_player)
                    threading.Thread(target=request_random_step).start()  # To be replaced with the Maximal algorithm function
                    return 1
                elif res == 2 and win == TIE:
                    threading.Timer(2, next_round, args=(True,)).start()
                elif res == 2:  # Successful, and ended, so comes the next round
                    round_list[current_round] = current_player
                    roundend_event.set()
                    # TODO: Feldolgozni a nyerést a grafikus felületen, és az új kör kezdetét
                    threading.Timer(2, next_round).start()
                    return 2
                return res
            else:
                if res == 1:  # Successful, so Player turn
                    current_player = not current_player
                    # TODO: Grafikus feluleten megjeleniteni, hogy a Player1 jon
                    return 1
                elif res == 2 and win == TIE:
                    threading.Timer(2, next_round, args=(True,)).start()
                elif res == 2:  # Successful, and ended, so comes the next round
                    round_list[current_round] = current_player
                    roundend_event.set()
                    # TODO: Feldolgozni a nyerést a grafikus felületen, és az új kör kezdetét
                    threading.Timer(2, next_round).start()
                    return 1
                return res
        elif game_type == GAME_SAMEPC:
            if res == 1:  # Successful, so next player comes
                current_player = switch_player(current_player)
                return 1
            elif res == 2 and win == TIE:  # Successful, and tie, so restart the round
                threading.Timer(2, next_round, args=(True,)).start()
            elif res == 2:  # Successful, and ended, so comes the next round
                round_list[current_round] = current_player
                # TODO: Feldolgozni a nyerést a grafikus felületen, és az új kör kezdetét
                threading.Timer(2, next_round).start()
                return 2
            return res
    except Exception as e:
        sendError("Error in base_game.py/request_put", str(e))


def put(pos, letter):  # Returns: -1, if not empty; 0, if no space; 1, if successful; 2, if successful and game end
    try:
        global board_counter

        row, col = decode_pos(pos)
        if board[row][col] != EMPTY:
            return -1
        if board_counter == 9:
            return 0
        board[row][col] = letter

        board_counter += 1
        if letter == LETTER_O:
            txt = 'O'
        else:
            txt = 'X'
        msg = f'{pos} {txt}'
        queue.put(msg)  # The queue is used for displaying the elements on the GUI

        res, _ = check_win()
        if res == TIE:  # If the game is TIE
            print('The game finished TIE\n')
            print_board()
            return 2

        if res != NOT_ENDED:  # When we have a winner
            print(f'The winner is: {decode_player(current_player)} with letter {decode_letter(letter)}\n')
            print_board()
            return 2

        return 1
    except Exception as e:
        sendError("Error in base_game.py/put", str(e))


def request_random_step(t=2):  # For PVE
    # Putting on random pos
    time.sleep(t)
    random_pos = random.randint(1, 9)
    while request_put(random_pos, PLAYER_PC) != 1:
        random_pos = random.randint(1, 9)


def start_match(gt):  # Game types: GAME_PVP,GAME_PVE,GAME_SAMEPC; 3 round games
    try:
        global game_type, current_round, round_list, current_player, starting_player, match_ended

        clear_board(True)
        match_ended = False
        game_type = gt
        current_round = 1
        if game_type == GAME_PVE:
            starting_player = random.randint(PLAYER_PC, PLAYER_ME)
            current_player = starting_player

            print(f'The game has started! Starting player is: {decode_player(current_player)}\n')

            if starting_player == PLAYER_PC:
                threading.Thread(target=request_random_step, args=(0.5,)).start()

            pages.Ended.clear()
            pages.sixthpage()  # Calls GUI
            while True:  # This is used to reopen the GUI, because it can be called only from the main-loop
                pages.Closed.wait()
                if not match_ended:
                    pages.sixthpage()  # Calls GUI
                else:
                    break

            print('The match has ended!')
            pages.window.close()

        elif game_type == GAME_SAMEPC:
            starting_player = random.randint(PLAYER_ME, PLAYER_P2)
            current_player = starting_player

            print(f'The game has started! Starting player is: {decode_player(current_player)}\n')

            pages.Ended.clear()
            pages.sixthpage()  # Calls GUI
            while True:  # This is used to reopen the GUI, because it can be called only from the main-loop
                pages.Closed.wait()
                if not match_ended:
                    pages.sixthpage()  # Calls GUI
                else:
                    break
            print('The match has ended!')
    except Exception as e:
        sendError("Error in base_game.py/start_game", str(e))

