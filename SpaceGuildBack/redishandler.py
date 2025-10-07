import redis
import subprocess
import json

# START THE DOCKER CONTAINER
# docker run -d --name redis -p 6379:6379

# does the container exist?



subprocess.run("docker run -d --name redis -p 6379:6379".split(" "))

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


rh = redishandler()

rh.r.set('foo', 'bar')
# True
rh.r.get('foo')

