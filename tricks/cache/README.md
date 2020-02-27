Design and implement a data structure for a cache, which saves the most recently used key value pairs in a cache.
Note that the cache is a one to one mapping like a python dict, or C++ std::map.
 It should support the following operations: get and put.
get(key) - Get the value (will always be positive) of the key if the key exists in the cache, otherwise return -1.
put(key, value) - Set or insert the value if the key is not already present. When the cache reached its capacity,
it should invalidate the least recently used item before inserting a new item.
The cache is initialized with a positive capacity.

Can you do this in O(1) time complexity?
I have included two test harnesses, one in C++ another in python.
When creating sample input the input should be of the form:
cache_capacity
commands

commands are either:
put key value
or
get key

The file back_of_envelope_in.txt illustrates the format.
The file back_of_envelope_out.txt illustrates the expected output.
There are two larger examples of input and output, big_input.txt  big_output.txt which also illustrate the format.

I have included a sample test harness for python 3. The unit test currently do not work for python 2. I will fix this shortly.

One can choose to delete the unit test if one wants.
The expected performance is:
your_program < input.txt > output.txt

This is an optional performance:
your_program input.txt output.txt

The test harness once it is fully working will also support:
your_program test
To run the unit test.

I have included the python test harness. I will include the C++ and Java test harnesses shortly.
