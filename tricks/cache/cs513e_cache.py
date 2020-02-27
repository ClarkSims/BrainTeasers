#!/usr/bin/env python3
import unittest
import random
import sys


class MemNode:
    def __init__(self, key, val):
        self.prev = None
        self.next = None
        self.key = key
        self.val = val

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        nd = self
        retval = "{}".format(nd.val)
        nd = nd.next
        while nd is not None:
            retval += "->{}".format(nd.val)
            nd = nd.next
        return retval

    def len(self):
        rv = 0
        nd = self
        while nd is not None:
            rv += 1
            nd = nd.next
        return rv


class Cache(object):

    def __init__(self, capacity):
        """
        :type capacity: int
        """
        self.capacity = capacity
        self._kv_store = {}
        self._head = None
        self._tail = None
        self.size = 0
        self._node_store = [MemNode(0, 0) for _ in range(capacity)]

    def MemNodeFactory(self, key, val):
        assert self.size < self.capacity
        nd = self._node_store[self.size]
        nd.key = key
        nd.val = val
        self.size += 1
        return nd

    def get(self, key):
        """
        :type key: int
        :rtype: int
        """
        rv = -1
        if key in self._kv_store:
            nd = self._kv_store[key]
            rv = nd.val
            if nd != self._head:
                self._unlink_node(nd)
                self._make_head(nd)
        return rv

    def put(self, key, val):
        """
        :type key: int
        :type value: int
        :rtype: None
        """
        if key in self._kv_store:
            nd = self._kv_store[key]
            if nd != self._head:
                self._unlink_node(nd)
                self._make_head(nd)
            nd.val = val
        elif self.size < self.capacity:
            nd = self.MemNodeFactory(key, val)
            self._make_head(nd)
            if self.size == 1:
                self._tail = nd
        else:
            nd = self._tail
            self._unlink_tail()
            nd.key = key
            nd.val = val
            self._make_head(nd)

    def _make_head(self, nd):
        nd.next = self._head
        self._kv_store[nd.key] = nd
        if self._head is not None:
            self._head.prev = nd
        self._head = nd

    def _unlink_tail(self):
        if self._tail.prev != None:
            self._tail.prev.next = None
        nd = self._tail
        self._tail = self._tail.prev
        nd.prev = None
        del self._kv_store[nd.key]

    def _unlink_node(self, nd):
        if nd == self._tail:
            self._unlink_tail()
        else:
            nd.prev.next = nd.next
            nd.next.prev = nd.prev
            nd.next = nd.prev = None
            del self._kv_store[nd.key]

    def check(self):
        if self._head is not None:
            ln = self._head.len()
            assert ln == self.size
            self.check_list_integrity()
            assert ln == len(self._kv_store)
        else:
            assert 0 == len(self._kv_store)

    def check_list_integrity(self):
        assert self._head is not None
        prev = None
        nd = self._head
        while True:
            assert nd.prev == prev
            prev = nd
            if nd.next is None:
                break
            nd = nd.next
        assert self._tail == nd


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
            for _ in range(100):
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
            for _ in range(100):
                j = random.randint(0, i - 1)
                test = c.get(j)
                self.assertEqual(j, test)

            # repopulate the cache. all the old values will be overwritten
            # the new values will be key ^ 2
            for j in range(i):
                c.put(j, j * j)

            # randomly select keys, call get, and the return value should equal the key ^ 2
            for _ in range(100):
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
        cache.put(3, 3)  # evicts key 2
        self.assertEqual(cache.get(2), -1)  # returns -1 (not found)
        cache.put(4, 4)  # evicts key 1
        self.assertEqual(cache.get(1), -1)  # returns - 1(not found)
        self.assertEqual(cache.get(3), 3)
        self.assertEqual(cache.get(4), 4)


def execute_cache_algo(infile, outfile):
    first = True
    cache = None
    for line in infile:
        if first:
            first = False
            cache_size = int(line)
            cache = Cache(cache_size)
        else:
            tokens = line.split()
            if tokens[0] == 'put':
                if len(tokens) != 3:
                    print('each command must be in the format of get/put key value')
                key = int(tokens[1])
                value = int(tokens[2])
                cache.put(key, value)
            elif tokens[0] == 'get':
                key = int(tokens[1])
                value = cache.get(key)
                #print(value, file=outfile)
                outfile.write(str(value) + '\n')


def usage():
    '''
    Prints usage of program.
    '''
    print('The cache test program has three different modes')
    print('MYPROGRAM is the name that you have renamed the test template')
    print('This usage:"MYPROGRAM test" runs the unit test')
    print('This usage:"MYPROGRAM inputfile outputfile" reads from input file and writes to outputfile')
    print('This usage:"MYPROGRAM" reads from stdin and writes to stdout')
    print('The input must be in the following format:')
    print('NumberOfLines')
    print('Commands')
    print('each command is in the form "put key value" or "get key"')
    print('the file back_of_envelope_in.txt illustrates this format')


def main():
    '''
    Main function
    '''
    argc = len(sys.argv)
    if argc == 2:
        if sys.argv[1] == 'test':
            # unittest.main()
            print(
                'this is broken at the moment, in the meantime use "python[2|3] -m unittest"')
        else:
            usage()
    elif argc == 3:
        with open(sys.argv[1], 'r') as infile:
            with open(sys.argv[2], 'w') as outfile:
                execute_cache_algo(infile, outfile)
    elif argc == 1:
        execute_cache_algo(sys.stdin, sys.stdout)


if __name__ == '__main__':
    main()
