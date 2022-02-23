# from titration.utils import Titrator
# from pynput.keyboard import Listener
from pynput import keyboard

# titrator = Titrator.Titrator()

def run():
    # titrator.loop()
    pass

def log_keystroke(key):
    key = str(key).replace("'", "")

    if key == 'Key.space':
        key = ' '
    if key == 'Key.shift_r':
        key = ''
    if key == "Key.enter":
        key = '\n'

    with open("log.txt", 'a') as f:
        f.write(key)

# listener = keyboard.Listener(
#     on_press=log_keystroke,
#     on_release=run)
# listener.start()