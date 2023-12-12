import socket
import threading
import time
import re
import ping3
import sys
import os
import main
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'UI'))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'utils'))
import pages
import base_game
from utils.error import sendError
from utils.config import *

server_socket: socket.socket = None
May_Login = 0  # 0 - waiting, 1 succesful, 2 unsucc/username taken, 3 already logged in
listen_stop_flag = threading.Event()
Connected_To_Server = threading.Event()

enemy_move = False


def check_internet_connection():
    while not listen_stop_flag.is_set():
        time.sleep(2)
        try:
            ip_address = socket.gethostbyname(SERVER_IP)
            result = ping3.ping(ip_address, timeout=5)
            if result is None:
                print('There was a problem with the internet connection. Please check!\n')
                pages.Logout.set()
                return
        except Exception as e:
            sendError('Error in client.py/check_internet_connection', str(e))
    return


def stop_connection():
    if Connected_To_Server.is_set():
        listen_stop_flag.set()
    print('You have been disconnected from the server!')
    Connected_To_Server.clear()


def process_msg(msg):
    global May_Login

    if msg == 'auth suc':  # Successful authentication, can log in
        May_Login = 1
        send_message('get-rank')
        send_message('get-online-player-nb')
        return
    elif msg == 'auth inc':  # Authentication not successful, incorrect pass/username taken on register
        May_Login = 2
        return
    elif msg == 'auth ali':
        May_Login = 3
        return

    if msg == 'Enemy ingame':
        pages.Ingame.set()
        return
    # If the player got an invitation
    m = re.match(r'game inv ([a-zA-Z0-9]+)', msg)
    if m:
        pages.enemy_name = m.group(1)
        pages.Got_Inv.set()
        return

    # The signal of the starting of the game with the starting player
    m = re.match(r'^starting ([a-zA-Z0-9]+)', msg)
    if m:
        starter = m.group(1)
        if starter == pages.player_name:
            base_game.starting_player = base_game.PLAYER_ME
        else:
            base_game.starting_player = base_game.PLAYER_P2
        pages.Accepted.set()
        return

    # During match, if the enemy moved
    m = re.match(r'^move ([0-9])', msg)
    if m:
        segm = int(m.group(1))
        base_game.request_put(segm, base_game.PLAYER_P2)
        return

    m = re.match(r'^all-players:(.*)', msg)
    if m:
        tmp = m.group(1).strip().split(' ')
        nb = len(tmp)
        remain = nb % 10
        pages.leaderboard_list.clear()
        page = []
        for a in tmp:
            page.append(a)
            if len(page) % 10 == 0 and len(page) != 0:
                pages.leaderboard_list.append(page.copy())
                page.clear()
        for i in range(10-remain):
            page.append(' ')

        pages.leaderboard_list.append(page)

        pages.Wait_For_Request.set()
        return

    if msg == 'online-players:':
        pages.players_list.clear()
        pages.players_list.append((' ', 0))
        pages.Wait_For_Request.set()
        return

    m = re.match(r'^online-players:(.*)', msg)
    if m:
        tmp = m.group(1).strip().split(' ')
        nb = len(tmp)
        remain = nb % 10
        pages.players_list.clear()
        page = []
        for a in tmp:
            b = a.split(',')
            page.append((b[0], int(b[1])))
            if len(page) % 10 == 0 and len(page) != 0:
                pages.players_list.append(page.copy())
                page.clear()

        pages.players_list.append(page)
        pages.Wait_For_Request.set()
        return

    m = re.match(r'player-rank: ([0-9]*)', msg)
    if m:
        pages.player_rank = int(m.group(1))
        return

    m = re.match(r'online-player-nb: ([0-9]*)', msg)
    if m:
        pages.online_players = int(m.group(1))
        return
    if msg == 'enemy refused':
        pages.Refused.set()
        return
    if msg == 'enemy disconnected':
        pages.Disconnected.set()
        return
    if msg == 'enemy canceled':
        pages.Canceled.set()
        return


def listen_to_server():
    while not listen_stop_flag.is_set():
        try:
            data = server_socket.recv(1024)
            if not len(data):
                print('maybe offline?')

            if DEBUG:
                print("Received from server: {}".format(data.decode('utf-8')))
            tmp = data.decode().split('\n')
            for msg in tmp:
                process_msg(msg)

        except TimeoutError:
            pass
        except ConnectionResetError:
            sendError('Server closed the connection', 'Most probably the server shut down!')
            break
    server_socket.close()
    Connected_To_Server.clear()


def auth(username, password, reg=False):
    try:
        if reg:
            server_socket.send(f'auth-reg: {username} {password}'.encode())
        else:
            server_socket.send(f'auth: {username} {password}'.encode())
        return True
    except Exception as e:
        sendError('Error in authentication', str(e))
        Connected_To_Server.clear()
        return False


def send_message(msg):
    try:
        server_socket.send(f'{msg}'.encode())
    except Exception as e:
        sendError('Error in sending a message to the server', str(e))


def connect_to_server():
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.settimeout(5)

    listen_stop_flag.clear()

    try:
        server_socket.connect((SERVER_IP, SERVER_PORT))
        print(f"Connection to the server({SERVER_IP}:{SERVER_PORT}) was successful!")
        # threading.Thread(target=check_internet_connection).start()
        Connected_To_Server.set()
        send_message('get-online-player-nb')
    except ConnectionRefusedError as e:
        sendError('An error occured in client.py/connect_to_server', 'Connection refused by the server! ' + str(e))
        return None
    except Exception as e:
        if str(e) != 'timed out':
            sendError('An error occured in client.py/connect_to_server', str(e))
        return None

    listen_th = threading.Thread(target=listen_to_server)
    listen_th.start()
    return 1

