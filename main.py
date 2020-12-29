from threading import Thread
from host.host import run_host
from client.player import run_player
from termcolor import colored


Thread(target = run_host).start()
Thread(target = run_player).start()
print(colored('both servers aahave started', 'green'))