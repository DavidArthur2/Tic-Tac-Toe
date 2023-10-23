import cv2  # Képfeldolgozásra használt könyvtár
import mediapipe as mp  # Képfelismerésre használt könyvtár -- Tartalmazza a TensorFlowot
from utils.error import sendError
from gesture_recognition import calcResult
import threading
from memory_profiler import profile

# Default variables
mp_hands = mp.solutions.hands  # Hasznalt class a kezfelismeresre
mp_drawing = mp.solutions.drawing_utils  # Hasznalt class a kezrajzolasra
hands_detector = None # A kepfelismero

cam = None

detection_confidence = 0.5
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
    return True

def capture_frame():

    while cam.isOpened():

        res, frame = cam.read()

        if not res:
            sendError("Hiba a kamerával", "Megszakadt a kapcsolat a kamerával!")
            return False

        process_frame(frame)

        if cv2.waitKey(5) & 0xFF == ord("q"):
            break

@profile
def process_frame(frame):
    cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    rec_img = hands_detector.process(frame)

    if (rec_img.multi_hand_landmarks):
        hand_landmarks = rec_img.multi_hand_landmarks[0]
        mp_drawing.draw_landmarks(frame, hand_landmarks, connections=mp_hands.HAND_CONNECTIONS)
        # calcResult(hand_landmarks)



    cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    cv2.imshow("Kep", frame)

@profile
def operate_recognition():
    global hands_detector

    if not initialize_camera():
        return

    hands_detector = mp_hands.Hands(max_num_hands=1, min_detection_confidence=detection_confidence,min_tracking_confidence=tracking_confidence)
    capture_frame()

    hands_detector.close()
    cam.release()
    cv2.destroyAllWindows()


threading.Thread(target=operate_recognition).start()
