import msvcrt



# class virtual_keyboard:
#
#     def __init__(self, send_socket):
#         self.send_socket = send_socket
#
#     def on_release(self, key):
#         try:
#             self.send_socket.send(format(key).encode())
#         except OSError or ConnectionResetError:  # in case server hangs up before client realises
#             return False  # end listener
#
#     def listen(self):
#         pass
import time
rn = time.time() + 10
while time.time() < rn:
    if msvcrt.kbhit():
        c = msvcrt.getch()
        print(c)