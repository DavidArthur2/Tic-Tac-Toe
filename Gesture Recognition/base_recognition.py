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
hand_segm = 0

detection_confidence = 0.7
tracking_confidence = 0.5


def initialize_camera():
    global cam
    cam = cv2.VideoCapture(0)

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
    global stop_cam, raw_frame, hand_segm

    try:
        cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)  # Mirroring the camera
        raw_frame = frame.copy()

        rec_img = hands_detector.process(frame)

        if rec_img.multi_hand_landmarks:
            hand_landmarks = rec_img.multi_hand_landmarks[0]
            gesture, hand_segm = recognize_gesture(hand_landmarks, frame)
            # print(gesture)
        else:
            gesture = 0
            hand_segm = 0

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
    global hands_detector, camInitialized

    # Initialize recognizer
    camInitialized.clear()
    if not initialize_camera():
        return
    camInitialized.set()

    # Start capturing and recognizing
    hands_detector = mp_hands.Hands(max_num_hands=1, min_detection_confidence=detection_confidence,
                                    min_tracking_confidence=tracking_confidence)
    capture_frame()

    # Release resources
    stop_recognition()



