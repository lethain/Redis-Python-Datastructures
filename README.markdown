[redis]: http://code.google.com/p/redis/ "Redis"
[redis-py]: http://github.com/andymccurdy/redis-py "Redis-Py"

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
    . ./

    # install it
    pip install -r requirements.txt
    python setup.py install


# Usage

This section covers how to use this library to interface with Redis.


## Dictionary via Redis Strings

Using the entire Redis cluster as a dictionary:


    >>> from redis_ds import redis_dict
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

Using Redis hashes we can store multiple dictionaries in
one Redis server.

    >>> from redis_ds import redis_hash_dict
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

We also have a kind-of-sort-off implementation of a list which
certainly doesn't have the full flexibility of a Python list,
but is persistent, synchronized and sharable.

    >>> from redis_ds import redis_list
    >>> x = redis_list.RedisList("my-list")
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


## Serializing Redis Values

Thanks to work by [@hhuuggoo](https://github.com/hhuuggoo), this library also
supports serializing values before storing them in Redis. Each class has a
serialized equivalent, for example the above hashmap example becomes:

    >>> from redis_ds import redis_hash_dict
    >>> y = redis_hash_dict.PickleRedisHashDict('some_other_key')
    >>> y
    {}
    >>> y['a'] = {'obj': 'ect'}
    >>> y
    {'a': {'obj': 'ect'}}
    >>> y['a']['obj']
    'ect'

The only difference is that

    >>> x = redis_dict.RedisDict()

is now replaced with:

    >>> x = redis_dict.PickleRedisHashDict()
