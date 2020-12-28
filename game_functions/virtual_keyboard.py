from pynput.keyboard import Listener
def on_press(key):
    print("Key pressed {0}".format(key))


def listen():
    bool = True
    with Listener(on_press=on_press) as listener:
        while(bool):
            bool
listen()