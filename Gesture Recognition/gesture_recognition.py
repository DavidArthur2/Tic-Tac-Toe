import mediapipe as mp
import cv2
import math
from recognition_utils import *


def recognize_gesture(hand_landmarks, frame):
    global previous_gesture

    pos_x, pos_y = calc_median_pos(hand_landmarks, frame)
    segm = calc_hand_segment(pos_x, pos_y)
    draw_frame(frame, pos_x, pos_y, hand_landmarks=hand_landmarks, show_grid=True, show_dot=True, show_segment=True)

    landmarks = hand_landmarks.landmark

    if get_angle_between_fingers(landmarks[0], landmarks[4], landmarks[8]) < 19 and \
            get_angle_between_fingers(landmarks[0], landmarks[8], landmarks[12]) < 8 and \
            get_angle_between_fingers(landmarks[0], landmarks[12], landmarks[16]) < 6 and \
            get_angle_between_fingers(landmarks[0], landmarks[16], landmarks[20]) < 8:
        gesture = CLOSED_PALM
        previous_gesture = CLOSED_PALM
    elif get_angle_between_fingers(landmarks[0], landmarks[4], landmarks[8]) > 23 and \
            get_angle_between_fingers(landmarks[0], landmarks[8], landmarks[12]) > 9 and \
            get_angle_between_fingers(landmarks[0], landmarks[12], landmarks[16]) > 7 and \
            get_angle_between_fingers(landmarks[0], landmarks[16], landmarks[20]) > 10:
        previous_gesture = OPEN_PALM
        gesture = OPEN_PALM
    else:
        gesture = previous_gesture

    return gesture, segm
