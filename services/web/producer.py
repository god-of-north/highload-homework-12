from random import choice
from datetime import datetime
import string

import redis
import greenstalk
from flask import Flask, request


app = Flask(__name__)

redis_rdb = redis.Redis(host='redis-rdb', port=6379)
redis_aof = redis.Redis(host='redis-aof', port=6379)
beanstalkd = greenstalk.Client(('beanstalkd', 11300))

beanstalkd_id = 0
redis_rdb_id = 0
redis_aof_id = 0


def generate_message(id, size):
    ret = f'{datetime.now()}|{id}|'
    size = size - len(ret)
    return ret  + ''.join(choice(string.digits+string.ascii_letters) for _ in range(size - len(ret)))

def get_params():
    size = request.args.get('size') # message size
    batch = request.args.get('batch') # batch size
    return int(size), int(batch)

@app.route("/publish_redis_rdb")
def publish_redis_rdb():
    global redis_rdb_id

    size, batch = get_params()

    if batch == 1:
        message = generate_message(redis_rdb_id, size)
        redis_rdb.rpush('REDIS_RDB_QUEUE', message)
        redis_rdb_id += 1
    else:
        p = redis_aof.pipeline()
        for _ in range(batch):
            message = generate_message(redis_rdb_id, size)
            redis_rdb.rpush('REDIS_RDB_QUEUE', message)
            redis_rdb_id += 1
        p.execute()

    return 'OK'

@app.route("/publish_redis_aof")
def publish_redis_aof():
    global redis_aof_id

    size, batch = get_params()

    if batch == 1:
        message = generate_message(redis_aof_id, size)
        redis_aof.rpush('REDIS_AOF_QUEUE', message)
        redis_aof_id += 1
    else:
        p = redis_aof.pipeline()
        for _ in range(batch):
            message = generate_message(redis_aof_id, size)
            redis_aof.rpush('REDIS_AOF_QUEUE', message)
            redis_aof_id += 1
        p.execute()

    return 'OK'

@app.route("/publish_beanstalkd")
def publish_beanstalkd():
    global beanstalkd_id

    size, batch = get_params()

    for _ in range(batch):
        message = generate_message(beanstalkd_id, size)
        beanstalkd.put(message)
        beanstalkd_id += 1

    return 'OK'
