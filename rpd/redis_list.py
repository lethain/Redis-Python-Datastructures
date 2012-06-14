import redis_config
import UserList

class RedisList(object):
    def __init__(self, list_key, redis_client=redis_config.CLIENT):
        self._client = redis_client
        self.list_key = list_key
        
    def serialize(self, obj):
        return obj
    
    def deserialize(self, obj):
        return obj

    def __len__(self):
        return self._client.llen(self.list_key)

    def __getitem__(self, key):
        if type(key) == int:
            return self.deserialize(self._client.lindex(self.list_key, key))
        elif hasattr(key, 'start') and hasattr(key, 'stop'):
            start = key.start or 0
            stop = key.stop or -1
            return self.deserialize(
                self._client.lrange(self.list_key, start, stop))
        else:
            raise IndexError

    def __setitem__(self, pos, val):
        val = self.serialize(val)                
        return self._client.lset(self.list_key, pos, val)

    def append(self, val, head=False):
        val = self.serialize(val)                        
        if head:
            return self._client.lpush(self.list_key, val)
        else:
            return self._client.rpush(self.list_key, val)

    def pop(self, head=False, blocking=False):
        if head and blocking:
            return self.deserialize(self._client.blpop(self.list_key)[1])
        elif head:
            return self.deserialize(self._client.lpop(self.list_key))
        elif blocking:
            return self.deserialize(self._client.brpop(self.list_key)[1])
        else:
            return self.deserialize(self._client.rpop(self.list_key))

    def __unicode__(self):
        return u"RedisList(%s)" % (self[0:-1],)

    def __repr__(self):
        return self.__unicode__()

class PickleRedisList(RedisList):
    def serialize(self, obj):
        return pickle.dumps(obj)
    
    def deserialize(self, obj):
        return pickle.loads(obj)
    
