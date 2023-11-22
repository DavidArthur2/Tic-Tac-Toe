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


if __name__ == '__main__':
    # a = threading.Thread(target=operate_recognition)
    # a.start()
    # threading.Thread(target=mouse_tracker.get_hover_segment).start()
    # camInitialized.wait()
    # print('Cam initialized!')
    # th = threading.Thread(target=start_match, args=(GAME_PVE,))
    # th.start()
    # th.join()
    # stop_recognition()
    # exit(-1)
    # threading.Thread(target=client.connect_to_server).start()
    pages.ninthpage()
