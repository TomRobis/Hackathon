from threading import Thread
from host import run_host
from player import run_player
from termcolor import colored


Thread(target = run_player).start()
Thread(target = run_host).start()
print(colored('both servers have started', 'green'))