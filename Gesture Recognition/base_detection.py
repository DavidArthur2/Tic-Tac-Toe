import cv2  # Képfeldolgozásra használt könyvtár
import mediapipe as mp  # Képfelismerésre használt könyvtár -- Tartalmazza a TensorFlowot
from utils.error import sendError

# Default variables
mp_hands = mp.solutions.hands  # Hasznalt class a kezfelismeresre
mp_drawing = mp.solutions.drawing_utils  # Hasznalt class a kezrajzolasra

cam = cv2.VideoCapture(0)

detection_confidence = 0.7
tracking_confidence = 0.5



def CheckCamera():
    if cam is None:
        sendError("Hiba a kameránál", "Nincs inicializálva a kamera!")
        return False
    result, o = cam.read()

    if not result:
        sendError("Hiba a kamera megnyitásánál", "Nem található a kiválasztott kamera, vagy nem lehet megnyitni!")
        return False
    return True

def OperateCamera():
    if not CheckCamera():
        return

    while cam.isOpened():

        res, frame = cam.read()
        if not res:
            sendError("Hiba a kamerával", "Megszakadt a kapcsolat a kamerával!")
            return False

        cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        rec_img = mp_hands.Hands(max_num_hands=1, min_detection_confidence=detection_confidence,
                                 min_tracking_confidence=tracking_confidence).process(frame)

        cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        if rec_img.multi_hand_landmarks:
            for hand_landmarks in rec_img.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, connections=mp_hands.HAND_CONNECTIONS)
                x1 = float(str(rec_img.multi_hand_landmarks[-1].landmark[8]).split(' ')[1].split('\n')[0])
                x2 = float(str(rec_img.multi_hand_landmarks[-1].landmark[12]).split(' ')[1].split('\n')[0])
                x = abs((x1 - x2))
                cv2.putText(frame, f'Tavolsag a ket ujj kozott:{x}', (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)

        cv2.imshow("Kep", frame)

        if cv2.waitKey(5) & 0xFF == ord("q"):
            break

        cv2.waitKey(1)



OperateCamera()
