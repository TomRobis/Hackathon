from threading import Thread
from host import run_host
from player import run_player

Thread(target = run_player).start()
Thread(target = run_host).start()
print('both servers have started')