[redis]: http://code.google.com/p/redis/ "Redis"
[redis-py]: http://github.com/andymccurdy/redis-py "Redis-Py"

This package exposes [Redis][redis] backed datastructures which bring together
standard Python syntax with persistent in-memory storage. Redis operations
are all atomic as well, meaning that a thoughtful approach can use them
concurrently on multiple machines.

Utimately, a trivial wrapper around [Redis-Py][redis-py].

## Dictionary via Redis Strings

Using the entire Redis cluster as a dictionary:



    >>> import redis_dict
    >>> x = redis_dict.RedisDict()
    >>> x
    {}
    >>> x['a'] = 100
    >>> x
    {'a': '100'}
    >>> x['a']
    '100'
    >>> x['b']
    >>> len(x)
    1

## Dictionaries via Redis Hashes

Using Redis hashes we can split

    >>> import redis_hash_dict
    >>> x = redis_hash_dict.RedisHashDict("some_hash_key")
    >>> x
    {}
    >>> x['a'] = 100
    >>> x
    {'a': '100'}
    >>> x['a']
    '100'
    >>> x['b']
    >>> len(x)
    1

## Lists via Redis Lists

