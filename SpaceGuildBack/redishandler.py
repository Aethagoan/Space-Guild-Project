import redis
import subprocess
import json

# redis should be the token storage master.
# name = username?, contents = dict (or contents) is the rest.

class redishandler():
    def __init__(self):
        try:
            self.r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        except redis.ConnectionError as e:
            print(f"Failed to connect to Redis: {e}")
            raise

    def savedicttoredis(self, name, my_dict):
        try:
            self.r.set(name, json.dumps(my_dict).encode('utf-8'))
        except Exception as e:
            print(f"Failed to save dictionary to Redis: {e}")

    def getdictfromredis(self, name):
        try:
            return self.r.get(name)
        except Exception as e:
            print(f"Failed to retrieve dictionary from Redis: {e}")


