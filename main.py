import cv2
import threading
from gesture_recognition import detect_gesture, calculate_hand_distance
from mouse_control import gesture_mouse_control
from voice_control import recognize_voice_command, execute_command

# Initialize Webcam
cap = cv2.VideoCapture(0)
stop_flag = False  # Shared flag to stop both threads

def run_gesture_control():
    """Processes gestures from webcam."""
    global stop_flag

    while not stop_flag:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Webcam disconnected or unavailable!")
            break  # Exit loop if webcam fails

        # Detect gestures
        gesture = detect_gesture(frame)
        hand_distance = calculate_hand_distance(frame)  # Detect hand distance

        if gesture:
            print(f"Gesture Detected: {gesture}")

            if gesture == "left_click":
                print("Left Click Detected")
                gesture_mouse_control(action="left_click")

            elif gesture == "right_click":
                print("Right Click Detected")
                gesture_mouse_control(action="right_click")

        # Handle Minimize/Maximize Window based on hand distance
        if hand_distance:
            gesture_mouse_control(hand_distance=hand_distance)

        # Display frame
        cv2.imshow("Gesture Control", frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            stop_flag = True
            break

    cap.release()
    cv2.destroyAllWindows()

def run_voice_control():
    """Processes voice commands."""
    global stop_flag

    while not stop_flag:
        command = recognize_voice_command()
        if command:
            execute_command(command)

# Run Gesture & Voice Control in Parallel Threads
gesture_thread = threading.Thread(target=run_gesture_control, daemon=True)
voice_thread = threading.Thread(target=run_voice_control, daemon=True)

gesture_thread.start()
voice_thread.start()

# Wait for gesture thread to finish (stops both gracefully)
gesture_thread.join()
stop_flag = True  # Stop voice thread as well
voice_thread.join()
