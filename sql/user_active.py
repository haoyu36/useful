# coding=utf-8
import time
import random
from datetime import datetime

import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)
ACCOUNT_ACTIVE_KEY = 'account:active'

r.flushall()
now = datetime.utcnow()


def record_active(account_id, t=None):
    if t is None:
        t = datetime.utcnow()
    p = r.pipeline()
    key = ACCOUNT_ACTIVE_KEY
    for arg in ('year', 'month', 'day'):
        key = f'{key}:{getattr(t, arg)}'
        p.setbit(key, account_id, 1)
    p.execute()


def gen_records(max_days, population, k):
    for day in range(1, max_days):
        time_ = datetime(now.year, now.month, day)
        accounts = random.sample(range(population), k)
        for account_id in accounts:
            record_active(account_id, time_)


def calc_memory():
    r.flushall()

    print(f"USED_MEMORY: {r.info()['used_memory_human']}")

    start = time.time()

    gen_records(21, 1000000, 100000)

    print(f'COST: {time.time() - start}')
    print(f"USED_MEMORY: {r.info()['used_memory_human']}")

gen_records(29, 10000, 2000)
