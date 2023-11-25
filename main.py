import threading
import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Gesture Recognition'))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'utils'))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'UI'))
import base_recognition as br
import pages
from base_game import start_match, GAME_PVE, GAME_SAMEPC, GAME_PVP
import pyautogui
import mouse_tracker
import client


if __name__ == '__main__':
    # a = threading.Thread(target=br.operate_recognition)
    # a.start()
    # threading.Thread(target=mouse_tracker.get_hover_segment).start()
    # br.camInitialized.wait()
    # print('Cam initialized!')
    # th = threading.Thread(target=start_match, args=(GAME_PVE,))
    # th.start()
    # th.join()
    # br.stop_recognition()
    # exit(-1)
    # threading.Thread(target=client.connect_to_server).start()
    pages.seventhpage()
