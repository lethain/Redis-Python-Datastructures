[redis]: http://code.google.com/p/redis/ "Redis"
[redis-py]: http://github.com/andymccurdy/redis-py "Redis-Py"

*If you'd like to be a contributor, send me a note! I'd be more than glad to pass this over to a more active maintainer.*

This package exposes [Redis][redis] backed datastructures which bring together
standard Python syntax with persistent in-memory storage. Redis operations
are all atomic as well, meaning that a thoughtful approach can use them
concurrently on multiple machines.

Utimately, a trivial wrapper around [Redis-Py][redis-py].


## Simple Installation

   Ho hum. Having some setup.py issues I will have to resolve in a moment.


## Installation for development

For development, you should checkout the repository,
and install it into a [virtualenv](http://www.virtualenv.org/en/latest/):

    # get the code
    git clone https://github.com/lethain/Redis-Python-Datastructures.git
    cd Redis-Python-Datastructures.git

    # create and activate a virtualenv if you don't have one already
    virtualenv env
    . ./activate

    # install it
    pip install -r requirements.txt
    python setup.py install


## Running tests

With some embarassment, the tests currently run against local Redis using keys
prefixed with "test_rds.", and taking great pains not to delete any other keys,
so if you have a toy Redis node, the tests will not cause any harm, but you really
shouldn't run the tests against a Redis node you care deeply about.

Run them via:

    python src/redis_ds/tests.py

The tests really ought to be run against a mocked out version of Redis, but that
work hasn't been done yet.


# Usage

This section covers how to use this library to interface with Redis.


## Dictionary via Redis Strings

Using the entire Redis cluster as a dictionary:


    >>> from redis_ds.redis_dict import RedisDict
    >>> x = RedisDict()
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

Using Redis hashes we can store multiple dictionaries in
one Redis server.

    >>> from redis_ds.redis_hash_dict import RedisHashDict
    >>> x = RedisHashDict("some_hash_key")
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

We also have a kind-of-sort-off implementation of a list which
certainly doesn't have the full flexibility of a Python list,
but is persistent, synchronized and sharable.

    >>> from redis_ds.redis_list import RedisList
    >>> x = RedisList("my-list")
    >>> x
    RedisList([])
    >>> x.append("a")
    1
    >>> x.append("b")
    2
    >>> x
    RedisList(['a', 'b'])
    >>> x[0]
    'a'
    >>> x.pop()
    'b'
    >>> x
    RedisList(['a'])

It also provides access to blocking versions of pop, which
with a little creativity you can use to create a message queue
with workers.

    >>> x.pop(blocking=True)
    'a'

Woohoo.

## Sets

Sets are also available thanks to work by [@hhuuggoo])https://github.com/hhuuggoo):

    >>> from redis_ds.redis_set import RedisSet
    >>> x = RedisSet()
    >>> x.add("a")
    >>> x.add("a")
    >>> x.add("b")
    >>> x.add("b")
    >>> len(x)
    2
    >>> 'a' in x
    True
    >>> 'c' in x
    False
    >>> x.pop()
    'a'
    >>> len(x)
    1


## Serializing Values Stored in Redis

Thanks to work by [@hhuuggoo](https://github.com/hhuuggoo), this library also
supports serializing values before storing them in Redis. Each class has a
serialized equivalent, for example the above hashmap example becomes:

    >>> from redis_ds.redis_hash_dict import PickleRedisHashDict
    >>> y = PickleRedisHashDict('some_other_key')
    >>> y
    {}
    >>> y['a'] = {'obj': 'ect'}
    >>> y
    {'a': {'obj': 'ect'}}
    >>> y['a']['obj']
    'ect'

The same can be done using JSON instead of Pickle by changing it to:

    >>> from redis_ds.redis_hash_dict import JSONRedisHashDict

and so on. The same is true for ``RedisList`` which has ``PickleRedisList``
and ``JSONRedisList``, and so on.