import mediapipe as mp
import cv2
import math
from recognition_utils import *


def recognize_gesture(hand_landmarks, frame):
    global previous_gesture

    pos_x, pos_y = calc_median_pos(hand_landmarks, frame)
    draw_frame(frame, pos_x, pos_y, hand_landmarks=hand_landmarks, show_hand=True, show_grid=True, show_segment=True,
               show_pos=True)

    landmarks = hand_landmarks.landmark

    if get_angle_between_fingers(landmarks[0], landmarks[4], landmarks[8]) > 23 and \
            get_angle_between_fingers(landmarks[0], landmarks[8], landmarks[12]) > 9 and \
            get_angle_between_fingers(landmarks[0], landmarks[12], landmarks[16]) > 7 and \
            get_angle_between_fingers(landmarks[0], landmarks[16], landmarks[20]) > 10:
        previous_gesture = OPEN_PALM
        gesture = OPEN_PALM
    elif get_angle_between_fingers(landmarks[0], landmarks[4], landmarks[8]) < 18 and \
            get_angle_between_fingers(landmarks[0], landmarks[8], landmarks[12]) < 7 and \
            get_angle_between_fingers(landmarks[0], landmarks[12], landmarks[16]) < 5 and \
            get_angle_between_fingers(landmarks[0], landmarks[16], landmarks[20]) < 7:
        gesture = CLOSED_PALM
        previous_gesture = CLOSED_PALM
    else:
        gesture = previous_gesture

    return gesture
