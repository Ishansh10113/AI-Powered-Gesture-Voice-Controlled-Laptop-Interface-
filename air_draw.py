import cv2
import numpy as np

canvas = np.zeros((720, 1280, 3), dtype="uint8")

def draw_on_canvas(hand_landmarks):
    if hand_landmarks:
        x, y = int(hand_landmarks[8].x * 1280), int(hand_landmarks[8].y * 720)
        cv2.circle(canvas, (x, y), 5, (255, 0, 0), -1)
