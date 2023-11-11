import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'UI'))
import pages
import time
import pyautogui


def get_mouse_position_on_window():  # Returns the mouse position on the current window
    while pages.position is None:  # Window position
        time.sleep(0.1)
        continue

    (wx, wy) = pages.position
    (cx, cy) = pyautogui.position()

    x = cx - wx
    y = cy - wy

    if x < 0 or y < 0:
        x = y = 0

    return x, y


def get_mouse_segment():  # Returns the segment 1-9, 0 if something is wrong
    #while True:
     #   print(get_mouse_position_on_window())
    # button_positions[cell_id][top_left/bottom_right][x/y]
    button_positions = [
        {'top_left': {'x': 0, 'y': 0}, 'bottom_right': {'x': 0, 'y': 0}},  # 0 - Only for indexing
        {'top_left': {'x': 0, 'y': 0}, 'bottom_right': {'x': 0, 'y': 0}},  # 1
        {'top_left': {'x': 0, 'y': 0}, 'bottom_right': {'x': 0, 'y': 0}},  # 2
        {'top_left': {'x': 0, 'y': 0}, 'bottom_right': {'x': 0, 'y': 0}},  # 3
        {'top_left': {'x': 0, 'y': 0}, 'bottom_right': {'x': 0, 'y': 0}},  # 4
        {'top_left': {'x': 0, 'y': 0}, 'bottom_right': {'x': 0, 'y': 0}},  # 5
        {'top_left': {'x': 0, 'y': 0}, 'bottom_right': {'x': 0, 'y': 0}},  # 6
        {'top_left': {'x': 0, 'y': 0}, 'bottom_right': {'x': 0, 'y': 0}},  # 7
        {'top_left': {'x': 0, 'y': 0}, 'bottom_right': {'x': 0, 'y': 0}},  # 8
        {'top_left': {'x': 0, 'y': 0}, 'bottom_right': {'x': 0, 'y': 0}}  # 9
    ]

    for i in range(1,10):
        x1 = button_positions[i]['top_left']['x']
        y1 = button_positions[i]['top_left']['y']
        x2 = button_positions[i]['bottom_right']['x']
        y2 = button_positions[i]['bottom_right']['y']
#        if x1 <= x <= x2 and y1 <= y <= y2:
           # return i

    return 0
