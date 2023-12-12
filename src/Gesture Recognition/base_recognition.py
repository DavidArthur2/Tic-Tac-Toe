import cv2  # Képfeldolgozásra használt könyvtár
import mediapipe as mp  # Képfelismerésre használt könyvtár -- Tartalmazza a TensorFlowot
from utils.error import *
from gesture_recognition import recognize_gesture
import threading
from recognition_utils import *
from utils.config import *

# Default variables
hands_detector = None  # A kepfelismero
stop_cam = False

cam = None
raw_frame = None
camInitialized = threading.Event()
camInitFinished = threading.Event()
hand_segm = 0
cam_id = 0
cam_list = []
curr_gesture = 0
show_grid = False


def list_cameras():
    index = 0
    cam_list.clear()
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            break
        cam_list.append((index, cap.getBackendName()))
        cap.release()
        index += 1


def initialize_camera():
    global cam, cam_id
    list_cameras()

    if not len(cam_list):
        sendError('No camera found!', 'No camera found!', 0)
        cam_id = -1
        return True

    cam = cv2.VideoCapture(cam_id)  # Checking the actual camera(Double check)

    if cam is None:
        sendError("Error opening the cam", "The cam is not initialized, or no camera has been selected!")
        return False
    result, o = cam.read()

    if not result:
        sendError("Error opening the cam", "The cam is not initialized, or couldn't retrieve frame!")
        return False

    h, w, _ = o.shape  # Getting the default frame sizes of the camera
    set_cam_size(h, w)
    return True


def capture_frame():
    global cam_id
    while cam.isOpened() and not stop_cam:

        res, frame = cam.read()

        if not res and not stop_cam:
            sendError("Error capturing the frame", "The cam disconnected!", 0)
            cam_id = -1
            return False

        process_frame(frame)


def process_frame(frame):
    global stop_cam, raw_frame, hand_segm, curr_gesture

    try:
        if stop_cam:  # Stop flag
            return

        cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)  # Mirroring the camera
        if not show_grid:
            raw_frame = frame.copy()  # Making a copy for the visualized frame

        rec_img = hands_detector.process(frame)  # Initiate hand recognizer on the frame

        if rec_img.multi_hand_landmarks:  # If hand was detected
            hand_landmarks = rec_img.multi_hand_landmarks[0]  # Take the first hand
            curr_gesture, hand_segm = recognize_gesture(hand_landmarks, frame)  # Run the gesture recognizer on the fram
        else:
            curr_gesture = 0
            hand_segm = 0  # If no hand was detected, default values

        if show_grid:  # If the player allowed the grids, make a copy of the frame after it was drawed
            raw_frame = frame.copy()

        # Visualizing the frame that is used for detections
        # cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        # h, w = get_cam_size()
        # cv2.resize(frame, (w, h))
        # cv2.imshow("Kep", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            stop_recognition()

    except Exception as e:
        utils.error.sendError("Error in base_recognition.py",
                              "Something went wrong in process_frame function! " + str(e))


def stop_recognition():  # Stop function for the recognition methods
    global stop_cam
    try:
        stop_cam = True
        cam.release()
        if hands_detector is not None:
            hands_detector.close()
        cv2.destroyAllWindows()

        print("Resources released successfully!")
    except AttributeError as _:
        pass
    except Exception as e:
        utils.error.sendError("Error in base_recognition.py",
                              "Something went wrong in stop_recognition function! " + str(e))


def operate_recognition():  # The initiating of the recognition module
    global hands_detector, camInitialized, stop_cam

    stop_cam = False
    # Initialize recognizer
    camInitialized.clear()
    camInitFinished.clear()
    if not initialize_camera():
        camInitFinished.set()
        return
    camInitFinished.set()
    camInitialized.set()
    # Initializing finished

    if cam_id == -1:  # If no camera available
        stop_recognition()
        return

    # Start capturing and recognizing
    hands_detector = mp_hands.Hands(max_num_hands=1, min_detection_confidence=detection_confidence,
                                    min_tracking_confidence=tracking_confidence)
    capture_frame()

    # Release resources after stopped
    stop_recognition()



