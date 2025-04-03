import speech_recognition as sr
import pyautogui
import pyttsx3
import time
import keyboard

# Initialize Text-to-Speech engine
engine = pyttsx3.init()
recognizer = sr.Recognizer()

def speak(text):
    """Speak out the given text."""
    engine.say(text)
    engine.runAndWait()

def recognize_voice_command():
    """Recognize voice command from the microphone."""
    with sr.Microphone() as source:
        print("🎤 Listening for commands...")
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Reduce background noise
        
        try:
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=5)  # Adjusted timeout
            command = recognizer.recognize_google(audio).lower()
            print(f"✅ Recognized Command: {command}")
            return command
        
        except sr.UnknownValueError:
            print("❌ Could not understand the command.")
            return None
        
        except sr.RequestError:
            print("⚠️ Speech recognition service is unavailable.")
            return None
        
        except sr.WaitTimeoutError:
            print("⏳ No voice detected, please try again.")
            return None

def execute_command(command):
    """Execute commands based on recognized voice input."""
    if command is None:
        return

    # 🎮 GAME CONTROLS 🎮
    if "jump" in command:
        pyautogui.press("space")
        speak("Jumping!")

    elif "move straight" in command:
        keyboard.press("w")  # Hold 'W' key for forward movement
        speak("Moving forward!")

    elif "stop" in command:
        keyboard.release("w")  # Release 'W' key to stop movement
        speak("Stopping!")

    elif "go left" in command:
        keyboard.press("a")
        time.sleep(0.5)
        keyboard.release("a")
        speak("Turning left!")

    elif "go right" in command:
        keyboard.press("d")
        time.sleep(0.5)
        keyboard.release("d")
        speak("Turning right!")

    elif "reverse" in command:
        keyboard.press("s")
        time.sleep(0.5)
        keyboard.release("s")
        speak("Reversing!")

    elif "accelerate" in command:
        keyboard.press("up")  # Press Up Arrow for acceleration
        speak("Accelerating!")

    elif "brake" in command:
        keyboard.press("down")  # Press Down Arrow for braking
        speak("Braking!")

    # 📝 TEXT & APP CONTROLS 📝
    elif "open notepad" in command:
        pyautogui.hotkey('win', 'r')
        time.sleep(0.5)
        pyautogui.write("notepad")
        pyautogui.press("enter")
        speak("Opening Notepad.")

    elif "open word" in command:
        pyautogui.hotkey('win', 'r')
        time.sleep(0.5)
        pyautogui.write("winword")
        pyautogui.press("enter")
        speak("Opening Microsoft Word.")

    elif "type message" in command:
        speak("What should I type?")
        message = recognize_voice_command()
        if message:
            pyautogui.write(message)
            speak("Message typed.")

    elif "open whatsapp" in command:
        pyautogui.hotkey('win', 'r')
        time.sleep(0.5)
        pyautogui.write("whatsapp")
        pyautogui.press("enter")
        speak("Opening WhatsApp.")

    elif "send message" in command:
        speak("What should I send?")
        message = recognize_voice_command()
        if message:
            pyautogui.write(message)
            pyautogui.press("enter")
            speak("Message sent.")

    # 🔊 SYSTEM CONTROLS 🔊
    elif "increase volume" in command:
        pyautogui.press("volumeup", presses=5)
        speak("Increasing volume.")

    elif "decrease volume" in command:
        pyautogui.press("volumedown", presses=5)
        speak("Decreasing volume.")

    elif "mute" in command:
        pyautogui.press("volumemute")
        speak("Muting audio.")

    elif "lock screen" in command:
        pyautogui.hotkey("win", "l")
        speak("Locking your computer.")

    elif "shutdown" in command:
        speak("Are you sure you want to shut down? Say yes or no.")
        confirm = recognize_voice_command()
        if confirm and "yes" in confirm:
            speak("Shutting down your computer.")
            pyautogui.hotkey("win", "r")
            time.sleep(0.5)
            pyautogui.write("shutdown /s /t 5")
            pyautogui.press("enter")
        else:
            speak("Shutdown canceled.")

    else:
        print(f"❓ Command '{command}' not recognized.")
        speak(f"Command '{command}' not recognized.")

if __name__ == "__main__":
    while True:
        command = recognize_voice_command()
        if command:
            execute_command(command)
