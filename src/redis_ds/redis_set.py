"A Pythonic interface to a Redis set."
import redis_ds.redis_config as redis_config
from redis_ds.serialization import PassThroughSerializer, PickleSerializer


class RedisSet(PassThroughSerializer):
    "An object which behaves like a Python set, but which is based by Redis."
    def __init__(self, set_key, redis_client=redis_config.CLIENT):
        "Initialize the set."
        self._client = redis_client
        self.set_key = set_key
        
    def __len__(self):
        "Number of values in the set."
        return self._client.scard(self.set_key)

    def add(self, val):
        "Add a value to the set."
        val = self.serialize(val)
        self._client.sadd(self.set_key, val)
        
    def update(self, vals):
        "Idempotently Add multiple values to the set."
        vals = [self.serialize(x) for x in vals]
        self._client.sadd(self.set_key, *vals)
        
    def pop(self):
        "Remove and return a value from the set."
        return self.deserialize(self._client.spop(self.set_key))
    
    def remove(self, val):
        "Remove a specific value from the set."
        self._client.srem(self.set_key, self.serialize(val))
    
    def __unicode__(self):
        "Represent all members in a set."
        objs = self._client.smembers(self.set_key)
        objs = [self.deserialize(x) for x in objs]
        return u"RedisSet(%s)" % (objs,)

    def __repr__(self):
        "Represent all members in a set."
        return self.__unicode__()

class PickleRedisSet(RedisSet, PickleSerializer):
    "Pickle values stored in set."
    pass
    
