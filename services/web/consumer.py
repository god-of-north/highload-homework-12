import signal
from time import sleep
import threading

import redis
import greenstalk


redis_rdb = redis.Redis(host='redis-rdb', port=6379)
redis_aof = redis.Redis(host='redis-aof', port=6379)
beanstalkd = greenstalk.Client(('beanstalkd', 11300))


class GracefulKiller:
    kill_now = False
    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, *args):
        self.kill_now = True


def consume_beanstalkd():
    date = None
    id = None

    job = beanstalkd.reserve()
    if job is not None:
        date, id, _ = job.body.split('|')
        beanstalkd.delete(job)
    return date, id


def consume_rdb():
    date = None
    id = None

    data = redis_rdb.rpop('REDIS_RDB_QUEUE')
    if data is not None:
        date, id, _ = data.decode("utf-8") .split('|')
    return date, id

def consume_aof():
    date = None
    id = None

    data = redis_aof.rpop('REDIS_AOF_QUEUE')
    if data is not None:
        date, id, _ = data.decode("utf-8").split('|')
    return date, id

def try_print(date, id):
    if date!=None and id!=None:
        print("{: >20} {: >10}".format(date, id), flush=True)

def consume_worker(consume_func):
    while True:
        try_print(*consume_func())

if __name__ == '__main__':
    r1 = threading.Thread(name='consume_beanstalkd', daemon=True, target=lambda: consume_worker(consume_beanstalkd))
    r2 = threading.Thread(name='consume_rdb', daemon=True, target=lambda: consume_worker(consume_rdb))
    r3 = threading.Thread(name='consume_aof', daemon=True, target=lambda: consume_worker(consume_aof))

    r1.start()
    r2.start()
    r3.start()

    killer = GracefulKiller()
    while not killer.kill_now:
        sleep(1)

