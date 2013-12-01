"A pythonic interface to a Redis dictionary."
import redis_ds.redis_config as redis_config
from redis_ds.serialization import PassThroughSerializer, PickleSerializer, JSONSerializer


class RedisList(PassThroughSerializer):
    "Interface to a Redis list."
    def __init__(self, list_key, redis_client=redis_config.CLIENT):
        "Initialize interface."
        self._client = redis_client
        self.list_key = list_key

    def __len__(self):
        "Number of values in list."
        return self._client.llen(self.list_key)

    def __getitem__(self, key):
        "Retrieve a value by index or values by slice syntax."
        if type(key) == int:
            return self.deserialize(self._client.lindex(self.list_key, key))
        elif hasattr(key, 'start') and hasattr(key, 'stop'):
            start = key.start or 0
            stop = key.stop or -1
            values = self._client.lrange(self.list_key, start, stop)
            return [self.deserialize(value) for value in values]
        else:
            raise IndexError

    def __setitem__(self, pos, val):
        "Set the value at a position."
        val = self.serialize(val)
        return self._client.lset(self.list_key, pos, val)

    def append(self, val, head=False):
        "Append a value to list to rear or front."
        val = self.serialize(val)
        if head:
            return self._client.lpush(self.list_key, val)
        else:
            return self._client.rpush(self.list_key, val)

    def pop(self, head=False, blocking=False):
        "Remove an value from head or tail of list."
        if head and blocking:
            return self.deserialize(self._client.blpop(self.list_key)[1])
        elif head:
            return self.deserialize(self._client.lpop(self.list_key))
        elif blocking:
            return self.deserialize(self._client.brpop(self.list_key)[1])
        else:
            return self.deserialize(self._client.rpop(self.list_key))

    def __unicode__(self):
        "Represent entire list."
        return u"RedisList(%s)" % (self[0:-1],)

    def __repr__(self):
        "Represent entire list."
        return self.__unicode__()


class PickleRedisList(RedisList, PickleSerializer):
    "Serialize Redis List values via Pickle."
    pass


class JSONRedisList(RedisList, JSONSerializer):
    "Serialize Redis List values via JSON."
    pass
