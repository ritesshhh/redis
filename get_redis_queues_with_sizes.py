#import redis
import time
from django_redis import get_redis_connection


def take_redis_snap(**kwargs):
    print("<=== take_redis_snap running ===>")
    length = 0
    #r = redis.StrictRedis(host='localhost', port=6379, db=0)
    r = get_redis_connection("default")
    keys = r.keys('*')

    scard_list = r.keys("*es_thre*") # data types that uses scard command
    main_queues = r.keys("high*") # data types that uses llen command
    main_queues.extend(r.keys("low*"))
    main_queues.extend(r.keys("high*"))
    main_queues.extend(r.keys("critical*"))

    data = ""
    for key in keys:
        size = 0
        if key in scard_list:
            size = r.scard(key)
        elif key in main_queues:
            size = r.llen(key)
        if size > int(length):
            data = data + f"{str(key)}, size: {size} \n"
    if data:
        data = data + f"time : {time.asctime()} \n\n"
        with open('redis_snap.txt', 'a') as f:
            f.write(data)