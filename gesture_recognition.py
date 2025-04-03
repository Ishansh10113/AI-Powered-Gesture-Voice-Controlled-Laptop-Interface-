import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import speech_recognition as sr
import os
import time
import threading
import pygetwindow as gw
import win32gui
import win32con
import queue

# Reduce TensorFlow log warnings
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.8, min_tracking_confidence=0.8)
mp_draw = mp.solutions.drawing_utils

# Screen size for cursor movement
screen_w, screen_h = pyautogui.size()

# Cursor movement smoothing
prev_x, prev_y = 0, 0
smooth_factor = 0.3  # Adjusted for better balance

# Initialize Speech Recognizer
recognizer = sr.Recognizer()

# Speech Queue for Processing Commands
speech_queue = queue.Queue()

def recognize_speech():
    """Recognizes speech commands in a separate thread."""
    while True:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Faster adjustment
            print("🎤 Listening for voice commands...")

            try:
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=3)  # Reduced timeout
                command = recognizer.recognize_google(audio).lower()
                print(f"🎙️ Recognized: {command}")
                speech_queue.put(command)  # Add command to queue

            except sr.WaitTimeoutError:
                continue  # Skip if no command detected
            except sr.UnknownValueError:
                print("🔇 Could not understand audio.")
            except sr.RequestError:
                print("❌ Speech API error.")

def execute_voice_command(command):
    """Executes actions based on voice commands."""
    active_window = win32gui.GetForegroundWindow()  # Get the active window

    if command in ["minimize window", "minimize"]:
        win32gui.ShowWindow(active_window, win32con.SW_MINIMIZE)

    elif command in ["maximize window", "maximize"]:
        win32gui.ShowWindow(active_window, win32con.SW_MAXIMIZE)

    elif command in ["restore window"]:
        win32gui.ShowWindow(active_window, win32con.SW_RESTORE)  # Restore if minimized

    elif command in ["close window"]:
        win32gui.PostMessage(active_window, win32con.WM_CLOSE, 0, 0)  # Close window

    elif command in ["open notepad"]:
        os.system("notepad")

    elif command in ["open calculator"]:
        os.system("calc")

    elif command in ["open command prompt"]:
        os.system("start cmd")

    elif command in ["mute"]:
        pyautogui.press("volumemute")

    elif command in ["lock screen"]:
        os.system("rundll32.exe user32.dll,LockWorkStation")

    elif command in ["shutdown"]:
        os.system("shutdown /s /t 5")

def detect_gesture(frame):
    """Detects hand gestures and performs actions."""
    global prev_x, prev_y

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if not results.multi_hand_landmarks:
        return None  

    gesture_detected = None
    hand_positions = []

    for hand_landmarks in results.multi_hand_landmarks:
        landmarks = [(lm.x, lm.y) for lm in hand_landmarks.landmark]

        thumb_tip, index_tip, middle_tip, ring_tip = landmarks[4], landmarks[8], landmarks[12], landmarks[16]
        index_dip, middle_dip, ring_dip = landmarks[6], landmarks[10], landmarks[14]  

        # Cursor movement
        cursor_x = int(index_tip[0] * screen_w)
        cursor_y = int(index_tip[1] * screen_h)

        cursor_x = int(prev_x + (cursor_x - prev_x) * smooth_factor)
        cursor_y = int(prev_y + (cursor_y - prev_y) * smooth_factor)

        pyautogui.moveTo(cursor_x, cursor_y, duration=0.05)
        prev_x, prev_y = cursor_x, cursor_y  

        # Left Click (Middle Finger Closed)
        if middle_tip[1] > middle_dip[1]:  
            pyautogui.click()
            gesture_detected = "left_click"

        # Right Click (Ring Finger Closed)
        elif ring_tip[1] > ring_dip[1]:  
            pyautogui.click(button='right')
            gesture_detected = "right_click"

        hand_positions.append((landmarks[0][0], landmarks[0][1]))  

    # Minimize/Maximize Window Based on Distance Between Hands
    if len(hand_positions) == 2:
        distance = np.linalg.norm(np.array(hand_positions[0]) - np.array(hand_positions[1]))

        if distance < 0.10:  # Adjusted for better accuracy
            pyautogui.hotkey("win", "down")  # Minimize Window
            gesture_detected = "minimize"

        elif distance > 0.50:  # Adjusted for better accuracy
            pyautogui.hotkey("win", "up")  # Maximize Window
            gesture_detected = "maximize"

    # Volume Control Gestures (Pinch In / Out)
    if len(hand_positions) == 2:
        if distance < 0.15:  
            pyautogui.press("volumedown")  # Lower Volume
            gesture_detected = "volume_down"

        elif distance > 0.40:  
            pyautogui.press("volumeup")  # Increase Volume
            gesture_detected = "volume_up"

    return gesture_detected

# Start Voice Recognition in a Separate Thread
voice_thread = threading.Thread(target=recognize_speech, daemon=True)
voice_thread.start()

# Open webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1920)  # Maximize width for better taskbar accessibility
cap.set(4, 1080)  # Maximize height
cap.set(cv2.CAP_PROP_FPS, 30)

while True:
    success, frame = cap.read()
    if not success:
        print("❌ Error: Could not read frame from camera.")
        break

    frame = cv2.flip(frame, 1)  
    gesture = detect_gesture(frame)

    if gesture:
        print(f"✅ Gesture Detected: {gesture}")

    # Execute voice commands from queue
    if not speech_queue.empty():
        voice_command = speech_queue.get()
        execute_voice_command(voice_command)

    cv2.imshow("Gesture Control", frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):  
        break

cap.release()
cv2.destroyAllWindows()
