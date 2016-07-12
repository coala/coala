import time
import os

from coala_utils.decorators import enforce_signature
from coalib.output.printers.LogPrinter import LogPrinterMixin
from coalib.misc.CachingUtilities import (
    pickle_load, pickle_dump, delete_files)


class FileCache:
    """
    This object is a file cache that helps in collecting only the changed
    and new files since the last run. Example/Tutorial:

    >>> from pyprint.NullPrinter import NullPrinter
    >>> from coalib.output.printers.LogPrinter import LogPrinter
    >>> import logging
    >>> import copy, time
    >>> log_printer = LogPrinter()
    >>> log_printer.log_level = logging.CRITICAL

    To initialize the cache create an instance for the project:

    >>> cache = FileCache(log_printer, "test", flush_cache=True)

    Now we can track new files by running:

    >>> cache.track_files(["a.c", "b.c"])

    Since all cache operations are lazy (for performance), we need to
    explicitly write the cache to disk for persistence in future uses:
    (Note: The cache will automatically figure out the write location)

    >>> cache.write()

    Let's go into the future:

    >>> time.sleep(1)

    Let's create a new instance to simulate a separate run:

    >>> cache = FileCache(log_printer, "test", flush_cache=False)

    >>> old_data = copy.deepcopy(cache.data)

    We can mark a file as changed by doing:

    >>> cache.untrack_files({"a.c"})

    Again write to disk after calculating the new cache times for each file:

    >>> cache.write()
    >>> new_data = cache.data

    Since we marked 'a.c' as a changed file:

    >>> "a.c" not in cache.data
    True
    >>> "a.c" in old_data
    True

    Since 'b.c' was untouched after the second run, its time was updated
    to the latest value:

    >>> old_data["b.c"] < new_data["b.c"]
    True
    """

    @enforce_signature
    def __init__(
            self,
            log_printer: LogPrinterMixin,
            project_dir: str,
            flush_cache: bool=False):
        """
        Initialize FileCache.

        :param log_printer: An object to use for logging.
        :param project_dir: The root directory of the project to be used
                            as a key identifier.
        :param flush_cache: Flush the cache and rebuild it.
        """
        self.log_printer = log_printer
        self.project_dir = project_dir
        self.current_time = int(time.time())

        cache_data = pickle_load(log_printer, project_dir, {})
        last_time = -1
        if "time" in cache_data:
            last_time = cache_data["time"]
        if not flush_cache and last_time > self.current_time:
            log_printer.warn("It seems like you went back in time - your "
                             "system time is behind the last recorded run "
                             "time on this project. The cache will "
                             "be force flushed.")
            flush_cache = True

        self.data = cache_data.get("files", {})
        if flush_cache:
            self.flush_cache()

    def flush_cache(self):
        """
        Flushes the cache and deletes the relevant file.
        """
        self.data = {}
        delete_files(self.log_printer, [self.project_dir])
        self.log_printer.debug("The file cache was successfully flushed.")

    def __enter__(self):
        return self

    def write(self):
        """
        Update the last run time on the project for each file
        to the current time. Using this object as a contextmanager is
        preferred (that will automatically call this method on exit).
        """
        for file_name in self.data:
            self.data[file_name] = self.current_time
        pickle_dump(
            self.log_printer,
            self.project_dir,
            {"time": self.current_time, "files": self.data})

    def __exit__(self, type, value, traceback):
        """
        Update the last run time on the project for each file
        to the current time.
        """
        self.write()

    def untrack_files(self, files):
        """
        Removes the given files from the cache so that they are no longer
        considered cached for this and the next run.

        :param files: A set of files to remove from cache.
        """
        for file in files:
            if file in self.data:
                del self.data[file]

    def track_files(self, files):
        """
        Start tracking files given in ``files`` by adding them to the
        database.

        :param files: A set of files that need to be tracked.
                      These files are initialized with their last
                      modified tag as -1.
        """
        for file in files:
            if file not in self.data:
                self.data[file] = -1

    def get_uncached_files(self, files):
        """
        Returns the set of files that are not in the cache yet or have been
        untracked.

        :param files: The list of collected files.
        :return:      A set of files that are uncached.
        """
        if self.data == {}:
            # The first run on this project. So all files are new
            # and must be returned irrespective of whether caching is turned on.
            return files
        else:
            return {file
                    for file in files
                    if (file not in self.data or
                        int(os.path.getmtime(file)) > self.data[file])}
