import threading
import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Gesture Recognition'))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'utils'))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'UI'))
from base_recognition import operate_recognition
import pages
from base_game import start_match, GAME_PVE, GAME_SAMEPC, GAME_PVP
import pyautogui
import mouse_tracker


if __name__ == '__main__':
    # threading.Thread(target=operate_recognition).start()

    # th = threading.Thread(target=start_match, args=(GAME_PVE,)).start()
    # threading.Thread(target=mouse_tracker.get_mouse_segment()).start()
    pass

