import redis_config
import UserList

class RedisList(object):
    def __init__(self, list_key, redis_client=redis_config.CLIENT):
        self._client = redis_client
        self.list_key = list_key

    def __len__(self):
        return self._client.llen(self.list_key)

    def __getitem__(self, key):
        if type(key) == int:
            return self._client.lindex(self.list_key, key)
        elif hasattr(key, 'start') and hasattr(key, 'stop'):
            start = key.start or 0
            stop = key.stop or -1
            return self._client.lrange(self.list_key, start, stop)
        else:
            raise IndexError

    def __setitem__(self, pos, val):
        return self._client.lset(self.list_key, pos, val)

    def append(self, val, head=False):
        if head:
            return self._client.lpush(self.list_key, val)
        else:
            return self._client.rpush(self.list_key, val)

    def pop(self, head=False):
        if head:
            return self._client.lpop(self.list_key)
        else:
            return self._client.rpop(self.list_key)

    def __unicode__(self):
        return u"RedisList(%s)" % (self[0:-1],)

    def __repr__(self):
        return self.__unicode__()

