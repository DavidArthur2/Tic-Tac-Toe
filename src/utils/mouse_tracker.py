import os
import sys
import threading
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'UI'))
import pages
import time
import pyautogui
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'utils'))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Gesture Recognition'))
from error import sendError
import base_recognition

Stop_Mouse_Detect = threading.Event()  # Event for stopping the module


def get_mouse_position_on_window():  # Returns the calculated mouse position on the current window
    while pages.position is None and not Stop_Mouse_Detect.is_set():  # Waits for the GUI to start
        time.sleep(0.1)
        continue
    if Stop_Mouse_Detect.is_set():
        return None, None

    (wx, wy) = pages.position  # Get's the position of the GUI window
    (cx, cy) = pyautogui.position()  # Get's the position of the cursor

    x = cx - wx
    y = cy - wy

    if x < 0 or y < 0:
        x = y = 0

    return x, y  # Returns the relative mouse position on the window


def get_mouse_segment():  # Returns the segment 1-9, 0 if something is wrong
    x, y = get_mouse_position_on_window()
    if Stop_Mouse_Detect.is_set():
        return 0

    button_positions = [  # The positions of the 3x3 grid buttons on the game, ABSOLUTE VALUES
        {'top_left': {'x': 0, 'y': 0}, 'bottom_right': {'x': 0, 'y': 0}},  # 0 - Only for indexing
        {'top_left': {'x': 30, 'y': 192}, 'bottom_right': {'x': 161, 'y': 291}},  # 1
        {'top_left': {'x': 181, 'y': 192}, 'bottom_right': {'x': 313, 'y': 291}},  # 2
        {'top_left': {'x': 334, 'y': 192}, 'bottom_right': {'x': 465, 'y': 291}},  # 3
        {'top_left': {'x': 30, 'y': 299}, 'bottom_right': {'x': 161, 'y': 399}},  # 4
        {'top_left': {'x': 181, 'y': 299}, 'bottom_right': {'x': 313, 'y': 399}},  # 5
        {'top_left': {'x': 334, 'y': 299}, 'bottom_right': {'x': 465, 'y': 399}},  # 6
        {'top_left': {'x': 30, 'y': 409}, 'bottom_right': {'x': 161, 'y': 509}},  # 7
        {'top_left': {'x': 181, 'y': 409}, 'bottom_right': {'x': 313, 'y': 509}},  # 8
        {'top_left': {'x': 334, 'y': 409}, 'bottom_right': {'x': 465, 'y': 509}}  # 9
    ]

    for i in range(1, 10):  # Determining the boundaries of each cell/button, and checking on which the mouse is hovering
        x1 = button_positions[i]['top_left']['x']
        y1 = button_positions[i]['top_left']['y']
        x2 = button_positions[i]['bottom_right']['x']
        y2 = button_positions[i]['bottom_right']['y']
        if x1 <= x <= x2 and y1 <= y <= y2:
            return i

    return 0


def stop_hover_segment():  # Sets the stop signal for the module
    Stop_Mouse_Detect.set()


def get_hover_segment():  # This function combines the get_mouse_segment with the hand recognition hand segment
    try:
        Stop_Mouse_Detect.clear()
        while not Stop_Mouse_Detect.is_set():
            if not pages.Stopped.is_set():
                if base_recognition.hand_segm != 0:
                    pages.hover = base_recognition.hand_segm
                else:
                    pages.hover = get_mouse_segment()

            time.sleep(0.01)
        print('Getting segment of the hovered area stopped!')
    except Exception as e:
        sendError('Error in mouse_tracker/get_hover_segment', str(e))
