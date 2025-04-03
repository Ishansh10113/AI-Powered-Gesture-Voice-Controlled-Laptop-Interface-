import pyautogui

keyboard_mapping = {
    "open palm": "space",
    "index up": "enter",
    "thumb up": "volume up",
    "thumb down": "volume down"
}

def gesture_keyboard_control(gesture):
    if gesture in keyboard_mapping:
        pyautogui.press(keyboard_mapping[gesture])
