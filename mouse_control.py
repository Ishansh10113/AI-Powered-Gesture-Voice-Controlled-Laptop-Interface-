import pyautogui
import numpy as np

# Cursor smoothing variables
smoothening_factor = 3  # Adjust for better stability
prev_x, prev_y = 0, 0

# Previous hand distance to track movement
prev_hand_distance = None

def gesture_mouse_control(x=0, y=0, action=None, fingers=None, hand_distance=None):
    """Controls mouse actions based on gestures and hand distance."""
    global prev_x, prev_y, prev_hand_distance

    # Cursor Movement Smoothing
    if x and y:
        cur_x = (prev_x * (smoothening_factor - 1) + x) / smoothening_factor
        cur_y = (prev_y * (smoothening_factor - 1) + y) / smoothening_factor

        pyautogui.moveTo(cur_x, cur_y, duration=0.1)  # Smooth move
        prev_x, prev_y = cur_x, cur_y  # Update previous position

    # Perform Action Based on Gesture
    if action:
        if action == "left_click":
            pyautogui.click()
        elif action == "right_click":
            pyautogui.rightClick()
        return

    # Finger-Based Gesture Detection
    if fingers:
        # ✅ Left Click: Close **Middle Finger**
        if fingers == [0, 0, 1, 0, 0]:  
            pyautogui.click()

        # ✅ Right Click: Close **Ring Finger**
        elif fingers == [0, 0, 0, 1, 0]:  
            pyautogui.rightClick()

    # Hand Distance Detection for Minimize/Maximize
    if hand_distance is not None:
        if prev_hand_distance is not None:
            if hand_distance < prev_hand_distance - 30:  # Hands are coming close
                pyautogui.hotkey("win", "down")  # Minimize window
                print("Minimizing Window")
            elif hand_distance > prev_hand_distance + 30:  # Hands are moving apart
                pyautogui.hotkey("win", "up")  # Maximize window
                print("Maximizing Window")
        
        prev_hand_distance = hand_distance  # Update last hand distance
