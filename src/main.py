
import threading
import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Gesture Recognition'))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'utils'))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'UI'))
import base_recognition as br
from base_recognition import *
import pages
from base_game import start_match, GAME_PVE, GAME_SAMEPC, GAME_PVP
import pyautogui
import mouse_tracker
import client


cam_t = None
mouse_t = None
server_t = None
UI_t = None
program_stop_called = False


def stop_program():
    global program_stop_called
    if program_stop_called:
        return

    program_stop_called = True
    client.stop_connection()
    stop_recognition()
    mouse_tracker.stop_hover_segment()

    if cam_t is not None:
        cam_t.join()
    if mouse_t is not None:
        mouse_t.join()
    if UI_t is not None:
        UI_t.join()
    if server_t is not None:
        server_t.join()

    print('The program shut down!')


if __name__ == '__main__':
    print('Connecting to the server...')
    server_t = threading.Thread(target=client.connect_to_server)
    server_t.start()

    client.Connected_To_Server.wait(timeout=5)
    if not client.Connected_To_Server.is_set():
        print('Connection to the server failed...\n')
        stop_program()
        exit(1)

    print('Successfully connected to the server!\n')

    print('Initializing cam...')
    cam_t = threading.Thread(target=operate_recognition)
    cam_t.start()

    camInitialized.wait()
    print('Cam initialized!\n')

    print('Starting mouse position detector...')
    mouse_t = threading.Thread(target=mouse_tracker.get_hover_segment)
    mouse_t.start()
    print('Mouse position detector started!\n')

    print('Starting UI...')
    UI_t = threading.Thread(target=pages.firstpage)
    pages.firstpage()






# To start the application you shold call: client.connect_to_server - separate thread
# operate_recognition - separate thread
# mouse_tracker.get_hover_segment - separate thread
# firstpage - separate thread
# The start_match will be called from the UI