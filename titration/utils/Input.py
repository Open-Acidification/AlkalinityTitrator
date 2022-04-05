from pynput.keyboard import Key, Listener
import click, sys

keys = []
 
def getKey():
    return click.getchar()

def on_press(key):
    keys.append(''.format(key))
