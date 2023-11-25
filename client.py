import socket
import threading
import time
import re
import ping3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'UI'))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'utils'))
import pages
import base_game
from utils.error import sendError


server_socket: socket.socket = None
May_Login = 0  # 0 - waiting, 1 succesful, 2 unsucc/username taken
listen_stop_flag = threading.Event()

SERVER_PORT = 3356
SERVER_IP = socket.gethostname()

enemy_move = False


def check_internet_connection():
    while True:
        time.sleep(2)
        try:
            result = ping3.ping("google.com", timeout=2)
            if not result:
                print('There was a problem with the internet connection. Please check!')
                exit(-1)  # TODO: How to shutdown all threads
        except Exception as e:
            sendError('Error in client.py/check_internet_connection', str(e))


def stop_connection():
    listen_stop_flag.set()


def process_msg(msg):
    global May_Login

    if msg == 'auth suc':  # Successful authentication, can log in
        May_Login = 1
    elif msg == 'auth inc':  # Authentication not successful, incorrect pass/username taken on register
        May_Login = 2

    # If the player got an invitation
    m = re.match(r'game inv ([a-zA-Z0-9]+)', msg)
    if m:
        pages.Got_Inv.set()

    # The signal of the starting of the game with the starting player
    m = re.match(r'^starting ([a-zA-Z0-9]+)', msg)
    if m:
        starter = m.group(1)
        if starter == pages.player_name:
            base_game.starting_player = PLAYER_ME
        else:
            base_game.starting_player = PLAYER_P2
        pages.Accepted.set()

    # During match, if the enemy moved
    m = re.match(r'^move ([0-9])', msg)
    if m:
        segm = int(m.group(1))
        base_game.request_put(segm, PLAYER_P2)


def listen_to_server():
    while not listen_stop_flag.is_set():
        try:
            data = server_socket.recv(1024)
            if not data:
                raise ConnectionResetError

            print("Received from server: {}".format(data.decode('utf-8')))
            process_msg(data.decode('utf-8'))
        except TimeoutError:
            pass
        except ConnectionResetError:
            sendError('Server closed the connection', 'Most probably the server shut down!')
            break
    server_socket.close()
    print('You have been disconnected from the server!')
    exit(-1)


def auth(username, password, reg=False):
    try:
        if reg:
            server_socket.send(f'auth-reg: {username} {password}'.encode())
        else:
            server_socket.send(f'auth: {username} {password}'.encode())
    except Exception as e:
        sendError('Error in authentication', str(e))


def send_message(msg):
    try:
        server_socket.send(f'{msg}'.encode())
    except Exception as e:
        sendError('Error in sending a message to the server', str(e))


def connect_to_server():
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.settimeout(1)

    listen_stop_flag.clear()
    threading.Thread(target=check_internet_connection).start()

    try:
        server_socket.connect((SERVER_IP, SERVER_PORT))
        print(f"Connection to the server({SERVER_IP}:{SERVER_PORT}) was successful!")
    except ConnectionRefusedError as e:
        sendError('An error occured in client.py/connect_to_server', 'Connection refused by the server! ' + str(e))
        return None
    except Exception as e:
        sendError('An error occured in client.py/connect_to_server', str(e))
        return None

    listen_th = threading.Thread(target=listen_to_server)
    listen_th.start()
    return 1

