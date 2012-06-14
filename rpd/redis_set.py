import redis_config
import UserList
import cPickle as pickle

class RedisSet(object):
    def __init__(self, set_key, redis_client=redis_config.CLIENT):
        self._client = redis_client
        self.set_key = set_key
        
    def serialize(self, obj):
        return obj
    
    def deserialize(self, obj):
        return obj

    def __len__(self):
        return self._client.scard(self.set_key)

    def add(self, val):
        val = self.serialize(val)
        self._client.sadd(self.set_key, val)
        
    def update(self, vals):
        vals = [self.serialize(x) for x in vals]
        self._client.sadd(self.set_key, *vals)
        
    def pop(self):
        return self.deserialize(self._client.spop(self.set_key))
    
    def remove(self, val):
        self._client.srem(self.set_key, self.serialize(val))
    
    def __unicode__(self):
        objs = self._client.smembers(self.set_key)
        objs = [self.deserialize(x) for x in objs]
        return u"RedisSet(%s)" % (objs,)

    def __repr__(self):
        return self.__unicode__()

class PickleRedisSet(RedisSet):
    def serialize(self, obj):
        return pickle.dumps(obj)
    
    def deserialize(self, obj):
        return pickle.loads(obj)
    
