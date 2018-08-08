import logging
import time
import os

from coala_utils.decorators import enforce_signature
from coalib.misc.CachingUtilities import (
    pickle_load, pickle_dump, delete_files)
from coalib.misc.Exceptions import log_exception
from coalib.processes.Processing import get_file_dict
from coalib.io.FileProxy import (
    FileDictGenerator, FileProxy, FileProxyMap)
from coalib.output.printers.LOG_LEVEL import LOG_LEVEL


class FileCache:
    """
    This object is a file cache that helps in collecting only the changed
    and new files since the last run. Example/Tutorial:

    >>> import logging
    >>> import copy, time
    >>> logging.getLogger().setLevel(logging.CRITICAL)

    To initialize the cache create an instance for the project:

    >>> cache = FileCache(None, "test", flush_cache=True)

    Now we can track new files by running:

    >>> cache.track_files(["a.c", "b.c"])

    Since all cache operations are lazy (for performance), we need to
    explicitly write the cache to disk for persistence in future uses:
    (Note: The cache will automatically figure out the write location)

    >>> cache.write()

    Let's go into the future:

    >>> time.sleep(1)

    Let's create a new instance to simulate a separate run:

    >>> cache = FileCache(None, "test", flush_cache=False)

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
            log_printer,
            project_dir: str,
            flush_cache: bool = False):
        """
        Initialize FileCache.

        :param log_printer: An object to use for logging.
        :param project_dir: The root directory of the project to be used
                            as a key identifier.
        :param flush_cache: Flush the cache and rebuild it.
        """
        self.project_dir = project_dir
        self.current_time = int(time.time())

        cache_data = pickle_load(None, project_dir, {})
        last_time = -1
        if 'time' in cache_data:
            last_time = cache_data['time']
        if not flush_cache and last_time > self.current_time:
            logging.warning('It seems like you went back in time - your system '
                            'time is behind the last recorded run time on this '
                            'project. The cache will be force flushed.')
            flush_cache = True

        self.data = cache_data.get('files', {})
        if flush_cache:
            self.flush_cache()

        # store the files to be untracked and then untrack them in the end
        # so that an untracked file is not tracked again by mistake in a
        # later section (which will happen if that file doesn't yield a
        # result in that section).
        self.to_untrack = set()

    def flush_cache(self):
        """
        Flushes the cache and deletes the relevant file.
        """
        self.data = {}
        delete_files(None, [self.project_dir])
        logging.debug('The file cache was successfully flushed.')

    def __enter__(self):
        return self

    def write(self):
        """
        Update the last run time on the project for each file
        to the current time. Using this object as a contextmanager is
        preferred (that will automatically call this method on exit).
        """
        for file in self.to_untrack:
            if file in self.data:
                del self.data[file]
        for file_name in self.data:
            self.data[file_name] = self.current_time
        pickle_dump(
            None,
            self.project_dir,
            {'time': self.current_time, 'files': self.data})

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
        self.to_untrack.update(files)

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


class FileDictFileCache(FileCache, FileDictGenerator):
    """
    FileDictFileCache extends a traditional FileCache
    to support generation of a complete file dict, this
    lets FileDictFileCache provide access to both file
    cache and contents of files from disk.
    """

    def __init__(self, *args, **kargs):
        """
        This directly initializes the associated FileCache.
        """
        super().__init__(*args, **kargs)

    def get_file_dict(self, filename_list, allow_raw_files=False):
        """
        Returns a file dictionary mapping from filename to lines of
        file. Uses coalib.processes.Processing.get_file_dict().

        :param filename_list:   List of filenames as strings to build
                                the file dict.
        :param allow_raw_files: Indicates if the file could also be
                                read as a binary.
        :return:                Reads the content of each file into
                                dictionary with filenames as keys.
        """
        return get_file_dict(filename_list,
                             allow_raw_files=allow_raw_files)


class ProxyMapFileCache(FileCache, FileDictGenerator):
    """
    ProxyMapFileCache is a FileCache that also provides
    methods to produce a file dict from a FileProxyMap.

    >>> import logging
    >>> import tempfile
    >>> import copy, time
    >>> logging.getLogger().setLevel(logging.CRITICAL)

    >>> file = tempfile.NamedTemporaryFile(delete=False)
    >>> file.write(b'coala')
    5
    >>> file.close()

    A new instance of ProxyMapFileCache can be instantited:

    >>> proxycache = ProxyMapFileCache(None, "test")

    Before any action on the associated proxy map is carried
    out, the proxymap needs to be initialized/set using:

    >>> proxymap = FileProxyMap()
    >>> proxycache.set_proxymap(proxymap)

    A file dict can now be build using the underlying proxy
    map using:

    >>> proxy = FileProxy.from_file(file.name, None)
    >>> proxymap.add(proxy)
    True

    >>> file_dict = proxycache.get_file_dict([file.name])
    >>> file_dict[file.name]
    ('coala',)
    """

    def __init__(self, *args, **kargs):
        """
        This directly initializes the associated FileCache.
        """
        super().__init__(*args, **kargs)
        self.__proxymap = None

    @enforce_signature
    def set_proxymap(self, fileproxy_map: FileProxyMap):
        """
        Used to assign a ProxyMap, this is separate from
        the instance initialization method to keep the
        concerns separate.

        :param fileproxy_map:   FileProxyMap instance to build
                                the file dict from.
        """
        self.__proxymap = fileproxy_map

    def get_file_dict(self, filename_list, allow_raw_files=False):
        """
        Builds a file dictionary from filename to lines of the file
        from an associated FileProxyMap.

        :param filename_list:   List of files to get the contents of.
        :param allow_raw_files: Allow the usage of raw files (non text files),
                                disabled by default
        :return:                Reads the content of each file into dictionary
                                with filenames as keys.
        """
        if self.__proxymap is None:
            raise ValueError('set_proxymap() should be called to set proxymap'
                             'of ProxyMapFileCache instance')

        file_dict = {}
        for filename in filename_list:
            try:
                # Keep the binary mode turned off to maintain compatibility
                # with FileDictFileCache.get_file_dict().
                # filename is assumed to be normcased.
                proxy = self.__proxymap.resolve(filename,
                                                hard_sync=True,
                                                binary=False)

                file_lines = proxy.lines()
                file_dict[filename] = tuple(file_lines)
            except UnicodeDecodeError:
                if allow_raw_files:
                    file_dict[filename] = None
                    continue

                logging.warning("Failed to read file '{}'. It seems to contain "
                                'non-unicode characters. Leaving it out.'
                                .format(filename))

            except (OSError, ValueError) as exception:
                log_exception("Failed to read file '{}' because of an unknown "
                              'error. Leaving it out.'.format(filename),
                              exception,
                              log_level=LOG_LEVEL.WARNING)

        return file_dict
