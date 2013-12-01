"""
This is module contains RedisDict, which allows users to interact with
Redis strings using the standard Python dictionary syntax.

Note that this uses an entire Redis database to back the dictionary,
not a Redis hashmap. If you prefer an interface to a hashmap, the
``redis_hash_dict`` file does just that.
"""
import UserDict
import redis_ds.redis_config as redis_config
from redis_ds.serialization import PassThroughSerializer, PickleSerializer, JSONSerializer


class RedisDict(UserDict.DictMixin, PassThroughSerializer):
    "Dictionary interface to Redis database."
    def __init__(self, redis_client=redis_config.CLIENT):
        """
        Parameters:
        - redis_client: configured redis_client to use for all requests.
                        should be fine to monkey patch this to set the
                        default settings for your environment...
        """
        self._client = redis_client

    def keys(self, pattern="*"):
        "Keys for Redis dictionary."
        return self._client.keys(pattern)

    def __len__(self):
        "Number of key-value pairs in dictionary/database."
        return self._client.dbsize()

    def __getitem__(self, key):
        "Retrieve a value by key."
        return self.deserialize(self._client.get(key))

    def __setitem__(self, key, val):
        "Set a value by key."
        val = self.serialize(val)
        return self._client.set(key, val)

    def __delitem__(self, key):
        "Ensure deletion of a key from dictionary."
        return self._client.delete(key)

    def __contains__(self, key):
        "Check if database contains a specific key."
        return self._client.exists(key)

    def get(self, key, default=None):
        "Retrieve a key's value from the database falling back to a default."
        return self.__getitem__(key) or default


class PickleRedisDict(RedisDict, PickleSerializer):
    "Serialize redis dictionary values via pickle."
    pass


class JSONRedisDict(RedisDict, JSONSerializer):
    "Serialize redis dictionary values via JSON."
    pass
