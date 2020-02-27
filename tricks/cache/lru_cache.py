#!/usr/bin/env python3
import unittest
import random


class Cache(object):

    def __init__(self, capacity):
        """
        Initializes a cache with a given capcity.
        If capacity is <= 0, then an exception should be thrown.
        @param int: capacity - a positive integer.
        """
        pass

    def get(self, key):
        """
        Searches cache for a key. If the key is not present -1 is returned.
        The entry in the cache is marked as most recent.
        @param  int:  key
        @return  int: value of key in cache, or -1 if missing
        """
        pass

    def put(self, key, val):
        """
        Puts a key value pair into the cache. This will be marked as the most recent.
        If the size of the cache is less than capacity, then a new node will be used.
        If the cache is full, the oldest referenced node in the cache will be overwritten
        with the new key value pair.
        @param key int: key of key value pair
        @param value int: value of key value pair
        @return None
        """
        pass


class SimpleTest(unittest.TestCase):
    def test_empty(self):
        '''
        Tries to create a cache with an invalid capacity.
        '''
        try:
            s = Cache(0)
        except Exception as e:
            self.fail("Cache(0) raised {} unexpectedly!".format(e))

        try:
            s = Cache(-5)
        except Exception as e:
            self.fail("Cache(0) raised {} unexpectedly!".format(e))

    def test_insert1(self):
        '''
        Test inserting 1 objects into a caches of sizes 2 and 5.
        The both caches should correctly return values for that objects.
        '''
        cache = Cache(2)
        cache.put(1, 10)
        self.assertEqual(10, cache.get(1))

        cache = Cache(5)
        cache.put(1, 10)
        self.assertEqual(cache.get(1), 10)

    def test_insert2(self):
        '''
        Test inserting 2 objects into a caches of sizes 3 and 5.
        The both caches should correctly return values for both objects.
        '''
        cache = Cache(2)
        cache.put(1, 10)
        self.assertEqual(cache.get(1), 10)
        cache.put(2, 20)
        self.assertEqual(cache.get(1), 10)
        self.assertEqual(cache.get(2), 20)

        cache = Cache(5)
        cache.put(1, 10)
        self.assertEqual(cache.get(1), 10)
        cache.put(2, 20)
        self.assertEqual(cache.get(1), 10)
        self.assertEqual(cache.get(2), 20)

    def test_insert3(self):
        '''
        Test inserting 3 objects into a caches of sizes 3 and 5.
        The cache of size 3, should forget the first object.
        The cache of size 5, should correctly return values for all 3 objects.
        '''
        cache = Cache(2)
        cache.put(1, 10)
        self.assertEqual(cache.get(1), 10)
        cache.put(2, 20)
        self.assertEqual(cache.get(2), 20)
        self.assertEqual(cache.get(1), 10)
        cache.put(3, 30)  # kicks out 2
        self.assertEqual(cache.get(3), 30)
        self.assertEqual(cache.get(1), 10)
        self.assertEqual(cache.get(2), -1)

        cache = Cache(5)
        cache.put(1, 10)
        self.assertEqual(cache.get(1), 10)
        cache.put(2, 20)
        self.assertEqual(cache.get(2), 20)
        self.assertEqual(cache.get(1), 10)
        cache.put(3, 30)
        self.assertEqual(cache.get(1), 10)
        self.assertEqual(cache.get(2), 20)
        self.assertEqual(cache.get(3), 30)

    def test_random_shuffle(self):
        '''
        This test populates a cache, without exceeding the capcity of the cache.
        The keys are integers between 0 and 99. The values are the same as the key.
        '''

        for i in range(1, 100):
            c = Cache(i)
            for j in range(i):
                c.put(j, j)
            for k in range(100):
                j = random.randint(0, i - 1)
                test = c.get(j)
                self.assertEqual(j, test)

    def test_random_shuffle_and_rewrite(self):
        '''
        This test populates a cache, without exceeding the capcity of the cache.
        The keys are integers between 0 and 99. The values are functionaly derived from the key.
        The get function is called repeatedly. It should always find the key in the cache
        and return the value, which should be the same as the key.
        Also, the cache is reused for the two different functions. When the cache is repopulated,
        every key value pair is overwritten.
        '''

        for i in range(1, 100):
            # allocate cache of size i
            c = Cache(i)

            # populate the cache, with keys from 0, to i-1.
            # the values are the same as the keys
            for j in range(i):
                c.put(j, j)

            # randomly select keys, call get, and the return value should equal the key
            for k in range(100):
                j = random.randint(0, i - 1)
                test = c.get(j)
                self.assertEqual(j, test)

            # repopulate the cache. all the old values will be overwritten
            # the new values will be key ^ 2
            for j in range(i):
                c.put(j, j * j)

            # randomly select keys, call get, and the return value should equal the key ^ 2
            for k in range(100):
                j = random.randint(0, i - 1)
                test = c.get(j)
                self.assertEqual(j * j, test)

    def test_back_of_envelope(self):
        '''
        This is a simple example that test inserting 4 key value pairs into a cache of size 2.
        '''
        cache = Cache(2)
        cache.put(1, 1)
        cache.put(2, 2)
        self.assertEqual(cache.get(1), 1)
        self.assertEqual(cache.get(2), 2)
        cache.put(3, 3)  # evicts key 2
        self.assertEqual(cache.get(2), -1)  # returns -1 (not found)
        self.assertEqual(cache.get(1), 1)
        self.assertEqual(cache.get(3), 3)
        cache.put(4, 4)  # evicts key 1
        self.assertEqual(cache.get(1), -1)  # returns - 1(not found)
        self.assertEqual(cache.get(3), 3)
        self.assertEqual(cache.get(4), 4)


if __name__ == '__main__':
    unittest.main()
