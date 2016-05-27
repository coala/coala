import time
import os

from coalib.misc.CachingUtilities import (
    pickle_load, pickle_dump)
from coalib.output.printers.LogPrinter import LogPrinter


class FileCache:
    """
    This object is a cache that helps figuring out if a file was modified
    since the last run of a program.

    >>> from pyprint.NullPrinter import NullPrinter
    >>> from coalib.output.printers.LogPrinter import LogPrinter
    >>> import copy, time
    >>> log_printer = LogPrinter(NullPrinter())

    To initialize the cache create an instance for the project:

    >>> cache = FileCache(log_printer, "test", flush_cache=True)

    Now we can track new files by running:

    >>> cache.track_new_files(["a.c", "b.c"])

    Since all cache operations are lazy (for performance), we need to
    explicitly write the cache to disk for persistence in future uses:
    (Note: The cache will automatically figure out the write location)

    >>> cache.close()

    Let's go into the future:

    >>> time.sleep(1)

    Let's create a new instance to simulate a separate run:

    >>> cache = FileCache(log_printer, "test", flush_cache=False)

    >>> old_data = copy.deepcopy(cache.data)

    We can mark a file as changed by doing:

    >>> cache.untrack_file({"a.c"})

    Again write to disk after calculating the new cache times for each file:

    >>> cache.close()
    >>> new_data = cache.data

    Since we marked 'a.c' as a changed file:

    >>> old_data["a.c"] == new_data["a.c"]
    True

    Since 'b.c' was untouched after the second run, its time was updated
    to the latest value:

    >>> old_data["b.c"] < new_data["b.c"]
    True
    """

    @enforce_signature
    def __init__(self, log_printer: LogPrinter, project_dir: str, flush_cache: bool=False):
        """
        Initialize FileCache.

        :param log_printer: A LogPrinter object to use for logging.
        :param project_dir: The root directory of the project to be used
                            as a key identifier.
        :param flush_cache: Flush the cache and rebuild it.
        """
        self.log_printer = log_printer
        self.project_dir = project_dir
        self.current_time = time.time()

        last_time, self.data = pickle_load(log_printer, self.project_dir, (-1, {}))

        if last_time > self.current_time:
            log_printer.warn("It seems like you went back in time - your "
                             "system time is behind the last recorded run "
                             "time on this project. The cache will "
                             "be force flushed.")
            flush_cache = True

        if flush_cache:
            self.flush_cache()

    def flush_cache(self):
        """
        Flushes the cache! Yeah!
        """
        self.data = {}
        self.log_printer.info("The cache was flushed successfully.")

    def __enter__(self):
        return self

    def close(self):
        """
        Closes the cache (like a file object). You may not rely on the cache
        being persistent if this method is called. Using this object as a
        context manager is preferred and will call this method automatically
        on exit.
        """
        for file_name in self.data:
            if file_name not in self.changed_files:
                self.data[file_name] = self.current_time
        pickle_dump(self.log_printer, self.md5sum, (self.current_time, self.data))

    def __exit__(self, type, value, traceback):
        """
        Update the last run time on the project for each file
        to the current time.
        """
        self.close()

    def untrack_files(self, files):
        """
        Removes the given files from the cache so they are no longer considered
        cached for this and the next run.
        """
        for file in files:
            if file in self.data:
                del self.data[file]

    def track_files(self, files):
        """
        Tracks the given files with the cache. Files will be shown as changed
        for this run but will appear cached in the next run.

        >>> TODO!

        :param files:
        :return:
        """
        for file in files:
            if file not in self.data:
                self.data[file] = -1

    def get_uncached_files(self, files):
        """
        Returns the set of files that are not in the cache or have been modified since the last run. This function does
        not

        :param files: The list of collected files.
        :return:      The list of files that had changed since the last cache.
        """
        if self.data == {}:
            return files
        else:
            return {file
                    for file in files
                    if (file not in self.data or
                        int(os.path.getmtime(file)) > self.data[file])}
