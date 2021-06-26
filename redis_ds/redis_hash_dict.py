"""
Module contains RedisHashDict, which allows users to interact with Redis hashes
as if they were Python dictionaries.
"""
import redis_ds.redis_config as redis_config
from redis_ds.serialization import PassThroughSerializer, PickleSerializer, JSONSerializer
try:
    import UserDict
    _DictMixin = UserDict.DictMixin
except ImportError:
    from collections import UserDict
    from collections import MutableMapping as DictMixin
    _DictMixin = DictMixin

class RedisHashDict(_DictMixin, PassThroughSerializer):
    "A dictionary interface to Redis hashmaps."
    def __init__(self, hash_key, redis_client=redis_config.CLIENT):
        "Initialize the redis hashmap dictionary interface."
        self._client = redis_client
        self.hash_key = hash_key

    def keys(self):
        "Return all keys in the Redis hashmap."
        return self._client.hkeys(self.hash_key)

    def __len__(self):
        "Number of key-value pairs in the Redis hashmap."
        return self._client.hlen(self.hash_key)

    def __getitem__(self, key):
        "Retrieve a value from the hashmap."
        return self.deserialize(self._client.hget(self.hash_key, key))

    def __setitem__(self, key, val):
        "Set a key's value in the hashmap."
        val = self.serialize(val)
        return self._client.hset(self.hash_key, key, val)

    def __delitem__(self, key):
        "Ensure a key does not exist in the hashmap."
        return self._client.hdel(self.hash_key, key)

    def __contains__(self, key):
        "Check if a key exists within the hashmap."
        return self._client.hexists(self.hash_key, key)

    def get(self, key, default=None):
        "Retrieve a key's value or a default value if the key does not exist."
        return self.__getitem__(key) or default

    def __iter__(self):
        "Return iterator over dictionary keys"
        return iter(self.keys())


class PickleRedisHashDict(RedisHashDict, PickleSerializer):
    "Serialize hashmap values using pickle."
    pass


class JSONRedisHashDict(RedisHashDict, JSONSerializer):
    "Serialize hashmap values using JSON."
    pass
