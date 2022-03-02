from pynput.keyboard import Key, Listener
import click, sys

keys = []
 
def getKey():
    # if keys:
    #     return keys.pop(0)
    # else:
    #     return None
    # return ''.format(click.getchar())
    return click.getchar()

def on_press(key):
    keys.append(''.format(key))

# # Collect events until released
# with Listener(
#         on_press=on_press) as listener:
#     listener.join()
