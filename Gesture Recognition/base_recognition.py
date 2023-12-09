import cv2  # Képfeldolgozásra használt könyvtár
import mediapipe as mp  # Képfelismerésre használt könyvtár -- Tartalmazza a TensorFlowot
from utils.error import *
from gesture_recognition import recognize_gesture
import threading
from recognition_utils import *

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
detection_confidence = 0.7
tracking_confidence = 0.5


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
    global cam
    list_cameras()

    if not len(cam_list):
        sendError('Nincs kamera', 'Nincs észlelve kamera!')
        return False

    cam = cv2.VideoCapture(cam_id)

    if cam is None:
        sendError("Hiba a kameránál", "Nincs inicializálva a kamera!")
        return False
    result, o = cam.read()

    if not result:
        sendError("Hiba a kamera megnyitásánál", "Nem található a kiválasztott kamera, vagy nem lehet megnyitni!")
        return False

    h, w, _ = o.shape  # Getting the default frame sizes of the camera
    set_cam_size(h, w)
    return True


def capture_frame():
    while cam.isOpened() and not stop_cam:

        res, frame = cam.read()

        if not res and not stop_cam:
            sendError("Hiba a kamerával", "Megszakadt a kapcsolat a kamerával!")
            return False

        process_frame(frame)


def process_frame(frame):
    global stop_cam, raw_frame, hand_segm, curr_gesture

    try:
        cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)  # Mirroring the camera
        if not show_grid:
            raw_frame = frame.copy()

        rec_img = hands_detector.process(frame)

        if rec_img.multi_hand_landmarks:
            hand_landmarks = rec_img.multi_hand_landmarks[0]
            curr_gesture, hand_segm = recognize_gesture(hand_landmarks, frame)
        else:
            curr_gesture = 0
            hand_segm = 0

        if show_grid:
            raw_frame = frame.copy()
        cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        # h, w = get_cam_size()
        # cv2.resize(frame, (w, h))
        # cv2.imshow("Kep", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            stop_recognition()

    except Exception as e:
        utils.error.sendError("Error in base_recognition.py",
                              "Something went wrong in process_frame function! " + str(e))


def stop_recognition():
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


def operate_recognition():
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

    # Start capturing and recognizing
    hands_detector = mp_hands.Hands(max_num_hands=1, min_detection_confidence=detection_confidence,
                                    min_tracking_confidence=tracking_confidence)
    capture_frame()

    # Release resources
    stop_recognition()



