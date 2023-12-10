import cv2
import math
import mediapipe as mp
import utils.error
from utils.config import *

cam_size = (480, 640)
previous_gesture = CLOSED_PALM

mp_hands = mp.solutions.hands  # Used class for hand recognition
mp_drawing = mp.solutions.drawing_utils  # Used class for hand landmarks drawing


def set_cam_size(h, w):
    global cam_size
    cam_size = (h, w)


def get_cam_size():
    return cam_size


def calc_median_pos(hand_landmarks, frame):
    try:
        (h, w) = cam_size

        sum_x = 0.0
        sum_y = 0.0
        i = 0
        for landmark in hand_landmarks.landmark:
            x = int(landmark.x * w)
            y = int(landmark.y * h)

            if i == 5 or i == 9 or i == 13 or i == 17:
                sum_x = sum_x + x * 0.0875
                sum_y = sum_y + y * 0.0875
            elif i == 0:
                sum_x = sum_x + x * 0.15
                sum_y = sum_y + y * 0.15
            else:
                sum_x = sum_x + x * 0.03125
                sum_y = sum_y + y * 0.03125

            i += 1

        return int(sum_x), int(sum_y)
    except Exception as e:
        utils.error.sendError("Error in recognition_utils.py", "Cannot calculate median pos! " + str(e))
        return False


# 1 2 3
# 4 5 6
# 7 8 9
# 0 ha nem felismerhető - hiba
def calc_hand_segment(hand_x, hand_y):
    segment = 0
    (h, w) = cam_size

    if 0 <= hand_x < int(w/3):  # first column
        if 0 <= hand_y < int(h/3):  # first row
            segment = 1
        if int(h/3) <= hand_y < int(2*h/3):  # second row
            segment = 4
        if int(2*h/3) <= hand_y <= int(3*h/3):  # third row
            segment = 7

    if int(w/3) <= hand_x < int(2*w/3):  # second column
        if 0 <= hand_y < int(h/3):  # first row
            segment = 2
        if int(h/3) <= hand_y < int(2*h/3):  # second row
            segment = 5
        if int(2*h/3) <= hand_y <= int(3*h/3):  # third row
            segment = 8

    if int(2*w/3) <= hand_x <= int(3*w/3):  # first column
        if 0 <= hand_y < int(h/3):  # first row
            segment = 3
        if int(h/3) <= hand_y < int(2*h/3):  # second row
            segment = 6
        if int(2*h/3) <= hand_y <= int(3*h/3):  # third row
            segment = 9

    return segment


def draw_frame(frame, hand_x, hand_y, show_pos=False, show_segment=False, show_hand=False, hand_landmarks=None,
               show_angles=False, show_grid=False, show_dot=False):
    (h, w) = cam_size

    try:
        if show_pos:
            cv2.putText(frame, f'Position_x:{hand_x}, Position_y:{hand_y}', (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                        (0, 255, 0), 2)
        if show_dot:
            cv2.circle(frame, (hand_x, hand_y), 5, (0, 255, 0), -1)
        # X: 0 213 426 640
        # Y: 0 160 320 480
        if show_grid:
            cv2.line(frame, (int(w/3), 0), (int(w/3), int(h)), (0, 255, 255), 2)
            cv2.line(frame, (int(2*w/3), 0), (int(2*w/3), int(h)), (0, 255, 255), 2)

            cv2.line(frame, (0, int(h/3)), (int(3*w/3), int(h/3)), (0, 255, 255), 2)
            cv2.line(frame, (0, int(2*h/3)), (int(3*w/3), int(2*h/3)), (0, 255, 255), 2)

        if show_segment:
            segm = calc_hand_segment(hand_x, hand_y)
            if segm == 0 and DEBUG:
                utils.error.sendError("Warning in recognition_utils.py", "In draw_frame function the segment cannot "
                                                                         "be calculated!  ", 0)

            cv2.putText(frame, f'{segm}', (320, 240), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)

        if show_hand:
            mp_drawing.draw_landmarks(frame, hand_landmarks, connections=mp_hands.HAND_CONNECTIONS)

        if show_angles:
            a1 = get_angle_between_fingers(hand_landmarks.landmark[0], hand_landmarks.landmark[4],
                                           hand_landmarks.landmark[8])
            pos1 = (int(abs(hand_landmarks.landmark[4].x + hand_landmarks.landmark[8].x) * h / 2),
                    int(abs(hand_landmarks.landmark[4].y
                            + hand_landmarks.landmark[8].y) * w / 2))

            cv2.putText(frame, f'{a1}', pos1, cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                        (0, 255, 0), 2)
    except Exception as e:
        utils.error.sendError("Error in recognition_utils.py", "Cannot draw frame! " + str(e))
        return False


def get_angle_between_fingers(mid_point, finger_1, finger_2):
    try:

        f1 = (finger_1.x, finger_1.y)
        f2 = (finger_2.x, finger_2.y)
        m = (mid_point.x, mid_point.y)

        a = pow(abs(f1[0] - f2[0]), 2) + pow(abs(f1[1] - f2[1]), 2)
        b = pow(abs(f1[0] - m[0]), 2) + pow(abs(f1[1] - m[1]), 2)
        c = pow(abs(m[0] - f2[0]), 2) + pow(abs(m[1] - f2[1]), 2)

        angle = math.acos((b + c - a) / (2 * math.sqrt(c) * math.sqrt(b)))
        angle = angle / math.pi * 180  # In degree
        return angle
    except Exception as e:
        utils.error.sendError("Error in recognition_utils.py", "Cannot calculate angle! " + str(e))
        return False
