import socket
import threading
import time
import re
import ping3


server_socket: socket.socket = None
May_Login = 0  # 0 - waiting, 1 succesful, 2 unsucc/username taken
listen_stop_flag = threading.Event()


def check_internet_connection():
    while True:
        time.sleep(2)
        try:
            result = ping3.ping("google.com", timeout=2)
            if not result:
                print('There was a problem with the internet connection. Please check!')
                exit(-1)
        except Exception as e:
            print("Error:", e)


def stop_connection():
    listen_stop_flag.set()


def process_msg(msg):
    global May_Login

    if msg == 'auth suc':
        May_Login = 1
    elif msg == 'auth inc':
        May_Login = 2


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
            print('The server stopped working!')
            break
    server_socket.close()
    print('Listening to the server stopped, and disconnected from the server!')


def auth(username, password, reg=False):
    if reg:
        server_socket.send(f'auth-reg: {username} {password}'.encode())
    else:
        server_socket.send(f'auth: {username} {password}'.encode())


def send_message(msg):
    server_socket.send(f'{msg}'.encode())


def connect_to_server(hostname=socket.gethostname(), port=3356):
    global server_socket, listen_th
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.settimeout(1)

    listen_stop_flag.clear()
    threading.Thread(target=check_internet_connection).start()

    try:
        server_socket.connect((hostname, port))
        print("Connection successful!")
    except ConnectionRefusedError:
        print("Connection refused!")
        return None
    except Exception as e:
        print("An error occurred:", e)
        return None

    listen_th = threading.Thread(target=listen_to_server)
    listen_th.start()
    return 1

