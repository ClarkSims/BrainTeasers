#!/usr/bin/python
'''
    This is a template for reliable thread safe pools of worker threads. It is based
    on the code here https://www.tutorialspoint.com/python/python_multithreading.htm.
    I have added Barrier class, to insure that the worker threads are completely created
    before the parent thread does any work.
'''

from threading import Thread, Event, Lock, Semaphore
import sys
import time


class Barrier(object):
    '''
        A barrier based on semaphores, based on code from
        https://stackoverflow.com/questions/26622745/implementing-barrier-in-python2-7
    '''

    def __init__(self, num_pass):
        self.num_pass = num_pass
        self.count = 0
        self.mutex = Semaphore(1)
        self.barrier = Semaphore(0)

    def wait(self):
        ''' Blocks until all threads have executed wait '''
        self.mutex.acquire()
        self.count = self.count + 1
        self.mutex.release()
        if self.count == self.num_pass:
            self.barrier.release()
        self.barrier.acquire()
        self.barrier.release()


class WorkerThread(Thread):
    '''
    This is an example of what a WorkerThread might look like. The run
    method needs to be rewritten to do real work.
    '''
    def __init__(self, thread_id, name, work_list, queue_lock, start_barrier, exit_flag):
        Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.work_list = work_list
        self.queue_lock = queue_lock
        self.start_barrier = start_barrier
        self.exit_flag = exit_flag

    def run(self):
        '''
        This is a prototype of what a worker thread might do.
        '''
        print "Starting " + self.name
        self.start_barrier.wait()

        while not self.exit_flag:
            self.queue_lock.acquire()
            if not self.work_list:
                data = self.work_list.pop()
                print "%s processing %s queue size = %d" % (self.name, data, self.work_list.qsize())
                sys.stdout.flush()
            self.queue_lock.release()
            time.sleep(.01)

        self.queue_lock.acquire()
        print "Exiting " + self.name
        sys.stdout.flush()
        self.queue_lock.release()


def main():
    '''
    This is a prototype of what a parent thread might do.
    It creates the child threads, waits, executes some loops with sleep,
    then tells the child threads to hault execution. It joins the
    child threads, then returns.
    '''

    thread_list = ["Thread-1", "Thread-2", "Thread-3"]
    name_list = ["One", "Two", "Three", "Four", "Five"]
    start_barrier = Barrier(4)
    exit_flag = Event(True)
    queue_lock = Lock()
    work_list = []

    threads = []
    thread_id = 1

    # Fill the queue
    for word in name_list:
        work_list.append(word)

    # Create new threads
    for thread_name in thread_list:
        thread = WorkerThread(thread_id, thread_name, work_list,
                              queue_lock, start_barrier, exit_flag)
        thread.start()
        threads.append(thread)
        thread_id += 1

    start_barrier.wait()

    # Wait for queue to empty
    while not work_list:
        print 'len(work_list) = %d' % len(work_list)
        time.sleep(1)

    # Notify threads it's time to exit
    exit_flag.set()
    time.sleep(.5)
    print "Joining Main Thread"
    # Wait for all threads to complete
    for thrd in threads:
        thrd.join()
    print "Exiting Main Thread"


if __name__ == '__main__':
    main()
