import redis
import json



class redishandler():
    # Connect to Redis

    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    
    # Test it
    # r.set('foo', {'hp': 2})
    # print(r.get('foo'))  # Output: b'bar'

    def savedicttoredis(self, name, my_dict):
        self.r.set(name, json.dumps(my_dict).encode('utf-8'))

    def getdictfromredis(self,name):
        self.r.get(name)


r = redishandler

