#!/usr/bin/env python3
from cs513e_cache import Cache
import random
import sys


def main():
    cache_capacity = int(sys.argv[1])
    number_transaction = int(sys.argv[2])
    max_id = int(sys.argv[3])
    assert cache_capacity > 0
    assert number_transaction > 0
    assert max_id > 0
    cache = Cache(cache_capacity)
    print(cache_capacity)
    for _ in range(number_transaction):
        choice = random.randint(0, 1)
        key = random.randint(0, max_id)
        if choice == 0:  # put
            value = random.randint(0, max_id)
            #cache.put(key, value)
            print('put {} {}'.format(key, value))
        else:
            print('get {}'.format(key))


if __name__ == '__main__':
    main()
