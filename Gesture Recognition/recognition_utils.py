import cv2
import math
import mediapipe as mp

import utils.error

# DEFINES
OPEN_PALM = 1
CLOSED_PALM = 2
#

previous_gesture = CLOSED_PALM

mp_hands = mp.solutions.hands  # Used class for hand recognition
mp_drawing = mp.solutions.drawing_utils  # Used class for hand landmarks drawing


def calc_median_pos(hand_landmarks, frame):
    try:
        h, w, _ = frame.shape

        sum_x = 0
        sum_y = 0

        for landmark in hand_landmarks.landmark:
            x = int(landmark.x * w)
            y = int(landmark.y * h)

            sum_x += x
            sum_y += y

        sum_x /= len(hand_landmarks.landmark)
        sum_y /= len(hand_landmarks.landmark)
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
    if 0 <= hand_x < 213:  # first column
        if 0 <= hand_y < 160:  # first row
            segment = 1
        if 160 <= hand_y < 320:  # second row
            segment = 4
        if 320 <= hand_y <= 480:  # third row
            segment = 7

    if 213 <= hand_x < 426:  # second column
        if 0 <= hand_y < 160:  # first row
            segment = 2
        if 160 <= hand_y < 320:  # second row
            segment = 5
        if 320 <= hand_y <= 480:  # third row
            segment = 8

    if 426 <= hand_x <= 640:  # first column
        if 0 <= hand_y < 160:  # first row
            segment = 3
        if 160 <= hand_y < 320:  # second row
            segment = 6
        if 320 <= hand_y <= 480:  # third row
            segment = 9

    return segment


def draw_frame(frame, hand_x, hand_y, show_pos=False, show_segment=False, show_hand=False, hand_landmarks=None,
               show_angles=False, show_grid=False):
    try:
        if show_pos:
            cv2.putText(frame, f'Position_x:{hand_x}, Position_y:{hand_y}', (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                        (0, 255, 0), 2)
            cv2.circle(frame, (hand_x, hand_y), 5, (0, 255, 0), -1)
        # X: 0 213 426 640
        # Y: 0 160 320 480
        if show_grid:
            cv2.line(frame, (213, 0), (213, 480), (0, 255, 255), 2)
            cv2.line(frame, (426, 0), (426, 480), (0, 255, 255), 2)

            cv2.line(frame, (0, 160), (640, 160), (0, 255, 255), 2)
            cv2.line(frame, (0, 320), (640, 320), (0, 255, 255), 2)

        if show_segment:
            segm = calc_hand_segment(hand_x, hand_y)
            if segm == 0:
                utils.error.sendError("Warning in recognition_utils.py", "In draw_frame function the segment cannot "
                                                                         "be calculated!  ", 0)

            cv2.putText(frame, f'{segm}', (320, 240), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)

        if show_hand:
            mp_drawing.draw_landmarks(frame, hand_landmarks, connections=mp_hands.HAND_CONNECTIONS)

        if show_angles:
            a1 = get_angle_between_fingers(hand_landmarks.landmark[0], hand_landmarks.landmark[4],
                                           hand_landmarks.landmark[8])
            pos1 = (int(abs(hand_landmarks.landmark[4].x + hand_landmarks.landmark[8].x) * 480 / 2),
                    int(abs(hand_landmarks.landmark[4].y
                            + hand_landmarks.landmark[8].y) * 640 / 2))

            cv2.putText(frame, f'{a1}', pos1, cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                        (0, 255, 0), 2)
    except Exception as e:
        utils.error.sendError("Error in recognition_utils.py", "Cannot draw frame! " + str(e))
        return False


def get_angle_between_fingers(mid_point, finger_1, finger_2):  # Ujra irni abc
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
