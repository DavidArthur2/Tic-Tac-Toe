import threading
import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Gesture Recognition'))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'utils'))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'UI'))
from base_recognition import operate_recognition, camInitialized, stop_recognition
import pages
from base_game import start_match, GAME_PVE, GAME_SAMEPC, GAME_PVP
import pyautogui
import mouse_tracker
import client

cam_t = None
mouse_t = None
server_t = None
UI_t = None


def stop_program():
    stop_recognition()
    client.stop_connection()
    mouse_tracker.stop_hover_segment()

    if cam_t is not None:
        cam_t.join()
    if mouse_t is not None:
        mouse_t.join()
    if server_t is not None:
        server_t.join()
    if UI_t is not None:
        UI_t.join()

    print('The program shut down!')
    sys.exit()  # TODO: Megkerdezni a tanart miert nem all meg


if __name__ == '__main__':
    print('Initializing cam...')
    cam_t = threading.Thread(target=operate_recognition)
    cam_t.start()

    camInitialized.wait()
    print('Cam initialized!\n')

    print('Starting mouse position detector...')
    mouse_t = threading.Thread(target=mouse_tracker.get_hover_segment)
    mouse_t.start()
    print('Mouse position detector started!\n')

    print('Connecting to the server...')
    server_t = threading.Thread(target=client.connect_to_server)
    server_t.start()
    server_t.join()
    if client.Connected_To_Server.is_set():
        print('Successfuly connected to the server!\n')
    else:
        print('Connection to the server failed...\nCheck server up-state, and your internet connection!')
        stop_program()

    print('Starting UI...')
    UI_t = threading.Thread(target=pages.firstpage)
    UI_t.start()
    print('UI started!\n')


# Innen meghivando jatek elejen: client.connect_to_server - kulon thread
# operate_recognition - kulon thread
# mouse_tracker.get_hover_segment - kulon thread
# firstpage - kulon thread
# A start_match CSAK a pagekrol hivhato, NEM kulon threadkent, hogy nelegyen gond a main_loop threades faszsaggal
