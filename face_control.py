import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh.FaceMesh()

def detect_expression(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = mp_face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        return "Smiling"
    return "Neutral"
