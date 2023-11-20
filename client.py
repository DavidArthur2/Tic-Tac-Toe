import socket
import threading
import time

import ping3


server_socket: socket.socket = None


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


def listen_to_server():
    while True:
        data = server_socket.recv(1024)

        if not data:  # If connection is closed
            break

        print("Received from server: {}".format(data.decode('utf-8')))


def auth(username, password):
    server_socket.send(f'auth: {username} {password}'.encode())


def send_message(msg):
    server_socket.send(f'{msg}'.encode())


def connect_to_server(hostname=socket.gethostname(), port=3356):
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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

    threading.Thread(target=listen_to_server).start()
    return 1

