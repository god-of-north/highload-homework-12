import signal
from time import sleep

import redis


class GracefulKiller:
    kill_now = False
    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, *args):
        self.kill_now = True

def consume_worker():
    killer = GracefulKiller()
    while not killer.kill_now:
        sleep(1)
        print('Consumer alive', flush=True)

consume_worker()
