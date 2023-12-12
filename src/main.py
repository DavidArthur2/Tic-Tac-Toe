
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

# Threads definitions
cam_t = None
mouse_t = None
server_t = None
UI_t = None

program_stop_called = False  # For single calling stop_program function


def stop_program():  # The main function to stop the entire game. Called when exiting a window, or an error
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
    if server_t is not None:
        server_t.join()

    print('The program shut down!')
    #exit(0)


if __name__ == '__main__':  # The main process which starts the game and the side threads.

    # Server connection assigned as a separate thread
    print('Connecting to the server...')
    server_t = threading.Thread(target=client.connect_to_server)
    server_t.start()

    client.Connected_To_Server.wait(timeout=5)  # Assigning a timeout to the connection
    if not client.Connected_To_Server.is_set():
        print('Connection to the server failed...\n')
        stop_program()
        exit(1)
    print('Successfully connected to the server!\n')

    # Operating recognition as a separate thread(if camera available)
    print('Initializing cam...')
    cam_t = threading.Thread(target=operate_recognition)
    cam_t.start()

    camInitialized.wait()
    print('Cam initialized!\n')

    # Run mouse segment detector as a separate thread
    print('Starting mouse position detector...')
    mouse_t = threading.Thread(target=mouse_tracker.get_hover_segment)
    mouse_t.start()
    print('Mouse position detector started!\n')

    # Starting the GUI in the main thread
    print('Starting UI...')
    pages.firstpage()


# To start the application you shold call: client.connect_to_server - separate thread
# operate_recognition - separate thread
# mouse_tracker.get_hover_segment - separate thread
# firstpage - separate thread
# The start_match will be called from the UI
