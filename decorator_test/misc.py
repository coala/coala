import inspect
from threading import Thread
from queue import Empty
from multiprocessing import Value, Queue, Manager, Process
from coalib.misc.Enum import enum


class Result:
    def __init__(self, message, file=None, origin=None):
        self.message = message
        self.file = file
        self.origin = origin


# This decorator would add the `-> Result` annotation to the function!
def bear(function):
    def exec_bear(*args, **kwargs):
        for result in function(*args, **kwargs):
            if result.origin is None:  # Fill origin automatically
                result.origin = function.__name__
            yield result

    return exec_bear


@bear
def number_of_files(file_dict):
    return Result("Number of files is "+str(len(file_dict)))


def is_bear(function):
    return isinstance(inspect.getfullargspec(function).annotations["return"],
                      Result)


def execute_task(task,
                 result_queue,
                 master_queue,
                 shared_dict,
                 pool_queue_queue):
    function_id, task_id = task
    # Assuming python shared dict caches that stuff, each function should
    # only be transferred at most once per process
    function = shared_dict[function_id]
    task = shared_dict[task_id]

    kwargs = {}
    if ("pool" in inspect.getfullargspec(function).args or
        "pool" in inspect.getfullargspec(function).kwonlyargs):
        pool_queue = Queue()
        kwargs["pool"] = pool(shared_dict,
                              pool_queue,
                              master_queue,
                              result_queue)
        pool_queue_queue.put(pool_queue)

    for result in function(task, **kwargs):
        result_queue.put(function_id, task_id, result)


def coala_worker(master_queue,
                 result_queue,
                 shared_dict,
                 active,
                 pool_queue_queue):
    # Retry until all tasks are fully processed
    while active > 0:
        try:
            execute_task(master_queue.get(timeout=0.1),
                         result_queue,
                         master_queue,
                         shared_dict,
                         pool_queue_queue)
        except Empty:
            pass

    return 0


class pool:
    def __init__(self, shared_dict, pool_queue, master_queue, result_queue):
        """
        This pool needs a dedicated queue (pool_queue). No other pools or
        processes should write or read from/to it. The master queue is the
        normal task queue used by everyone.
        """
        self.pool_queue = pool_queue
        self.master_queue = master_queue
        self.result_queue = result_queue
        self.shared_dict = shared_dict

    def imap_unordered(self, function, tasks):
        self.pool_queue.put(function, tasks)

        # Use this process for working too, use shared value to end it when
        # the time comes.
        active = Value('i', 1)
        worker = Thread(target=coala_worker, args=(self.master_queue,
                                                   self.result_queue,
                                                   self.shared_dict,
                                                   active))
        worker.start()

        for task in tasks:
            yield self.pool_queue.get(timeout=None)
        active = 0
        worker.join()


def pool_queue_listener(pool_queue):
    pass


def master_process(bears, files):
    task_queue = Queue()
    result_queue = Queue()
    manager = Manager()
    shared_dict = manager.dict
    active = Value('d', 1)

    processes = [Process(target=coala_worker, args=(task_queue,
                                                    result_queue,
                                                    shared_dict,
                                                    active))]



# TODO master process spawns processes, puts tasks in queues
# TODO for each task we need to introspect if it wants a pool object. If it
# wants one, we need to create one with an extra queue to the master object
# isolated from the task queue. Master process spawns a thread for each pool
# that just forwards the tasks to the master_queue so all workers can do it.
# Upon receiving a result, the master process determines if it was requested
# by any pool and in case forwards it to that, if not check if it's a printable
# result object and forward it to the callback if applicable.
