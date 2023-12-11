import socket

DEBUG = True
SERVER_PORT = 3356
SERVER_IP = 'arthurpc.go.ro'

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

detection_confidence = 0.7
tracking_confidence = 0.5

OPEN_PALM = 1
CLOSED_PALM = 2
