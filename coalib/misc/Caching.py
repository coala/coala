import calendar
import time
import hashlib
import os

from coalib.misc.CachingUtilities import (
    pickle_load, pickle_dump, time_consistent, update_time_db,
    delete_cache_files)


class FileCache:
    """
    Example/Tutorial:

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

    >>> cache.write()

    Let's go into the future:

    >>> time.sleep(1)

    Let's create a new instance to simulate a separate run:

    >>> cache = FileCache(log_printer, "test", flush_cache=False)

    >>> old_data = copy.deepcopy(cache.data)

    We can mark a file as changed by doing:

    >>> cache.add_to_changed_files({"a.c"})

    Again write to disk after calculating the new cache times for each file:

    >>> cache.write()
    >>> new_data = cache.data

    Since we marked 'a.c' as a changed file:

    >>> old_data["a.c"] == new_data["a.c"]
    True

    Since 'b.c' was untouched after the second run, its time was updated
    to the latest value:

    >>> old_data["b.c"] < new_data["b.c"]
    True
    """

    def __init__(self, log_printer, project_dir, flush_cache=False):
        """
        Initialize FileCache.

        :param log_printer: A LogPrinter object to use for logging.
        :param project_dir: The root directory of the project to be used
                            as a key identifier.
        :param flush_cache: Flush the cache and rebuild it.
        """
        self.log_printer = log_printer
        self.project_dir = project_dir
        self.md5sum = hashlib.md5(self.project_dir.encode("utf-8")).hexdigest()
        self.current_time = calendar.timegm(time.gmtime())
        if not flush_cache and not time_consistent(log_printer, self.md5sum):
            log_printer.warn("It seems like you went back in time - your "
                             "system time is behind the last recorded run "
                             "time on this project. The cache will "
                             "be flushed and rebuilt.")
            flush_cache = True
        if not flush_cache:
            self.data = pickle_load(log_printer, self.md5sum, {})
        else:
            self.data = {}
            delete_cache_files(log_printer, [self.md5sum])
            log_printer.info("The file cache was successfully flushed.")
        self.changed_files = set()

    def __enter__(self):
        return self

    def write(self):
        """
        Update the last run time on the project for each file
        to the current time.
        """
        for file_name in self.data:
            if file_name not in self.changed_files:
                self.data[file_name] = self.current_time
        pickle_dump(self.log_printer, self.md5sum, self.data)
        update_time_db(self.log_printer, self.md5sum, self.current_time)
        self.changed_files = set()

    def __exit__(self, type, value, traceback):
        """
        Update the last run time on the project for each file
        to the current time.
        """
        self.write()

    def add_to_changed_files(self, changed_files):
        """
        Keep track of changed files in ``changed_files`` for future use in
        ``write``.

        :param changed_files: A set of files that had changed since the last
                              run time.
        """
        self.changed_files.update(changed_files)

    def track_new_files(self, new_files):
        """
        Start tracking new files given in ``new_files`` by adding them to the
        database.

        :param new_files: The list of new files that need to be tracked.
                          These files are initialized with their last
                          modified tag as -1.
        """
        for new_file in new_files:
            self.data[new_file] = -1

    def get_changed_files(self, files):
        """
        Extract the list of files that had changed (or are new) with respect to
        the cache data available.

        :param files: The list of collected files.
        :return:      The list of files that had changed since the last cache.
        """
        changed_files = []

        if self.data == {}:
            # The first run on this project. So all files are new
            # and must be returned irrespective of whether caching is turned on.
            new_files = files
        else:
            new_files = []
            for file_path in files:
                if file_path in self.data and self.data[file_path] > -1:
                    if int(os.path.getmtime(file_path)) > self.data[file_path]:
                        changed_files.append(file_path)
                else:
                    new_files.append(file_path)

        self.track_new_files(new_files)
        self.add_to_changed_files(changed_files)

        return changed_files + new_files
