import logging
from os import path

from coala_utils.FileUtils import detect_encoding
from coala_utils.decorators import (enforce_signature, generate_eq)


@generate_eq('filename')
class FileProxy:
    """
    ``FileProxy`` is responsible for providing access to
    contents of files and also provides methods to update
    the in memory content register of the said file.

    >>> import logging
    >>> import tempfile
    >>> file = tempfile.NamedTemporaryFile(delete=False)
    >>> file.write(b'bears')
    5
    >>> file.close()

    To create a new file proxy instance of a file:

    >>> proxy = FileProxy(file.name, None, 'coala')
    >>> proxy.contents()
    'coala'

    >>> proxy.lines()
    ('coala',)


    You can replace the file contents in-memory by using
    the replace method on a file proxy. Version tracking
    is a simple way FileProxy provides to handle external
    incremental updates to the contents.

    >>> proxy.replace('coala-update', 1)
    True
    >>> proxy.contents()
    'coala-update'
    >>> proxy.version
    1

    File Proxy instances can also be initialized from files
    using FileProxy.from_file(). Binary files are also
    supported using from_file.

    >>> proxy2 = FileProxy.from_file(file.name, None)
    >>> proxy2.contents()
    'bears'
    """

    def __init__(self, filename, workspace=None, contents=''):
        """
        Initialize the FileProxy instance with the passed
        parameters. A FileProxy instance always starts at
        a fresh state with a negative version indicating
        that no updating operation has been performed on it.

        :param filename:
            The name of the file to create a FileProxy of.
            The filename is internally normcased.
        :param workspace:
            The workspace/project this file belongs to.
            Can be None.
        :param contents:
            The contents of the file to initialize the
            instance with. Integrity of the content or the
            sync state is never checked during initialization.
        """
        logging.debug('File proxy for {} created'.format(filename))

        # The file may not exist yet, hence there is no
        # reliable way of knowing if it is a file on the
        # disk or a directory.
        if not path.isabs(filename) or filename.endswith(path.sep):
            raise ValueError('expecting absolute filename')

        self._version = -1
        self._contents = contents
        self._filename = path.normcase(filename)
        self._workspace = workspace and path.normcase(workspace)

    def __str__(self):
        """
        :return:
            Return a string representation of a file proxy
            with information about its version and filename.
        """
        return '<FileProxy {}, {}>'.format(
            self._filename, self._version)

    def __hash__(self):
        """
        :return:
            Returns hash of the instance.
        """
        return hash(self.filename)

    def replace(self, contents, version):
        """
        The method replaces the content of the proxy
        entirely and does not push the change to the
        history. It is similar to updating the proxy
        with the range spanning to the entire content.

        :param contents:
            The new contents of the proxy.
        :param version:
            The version number proxy upgrades to after
            the update. This needs to be greater than
            the current version number.
        :return:
            Returns a boolean indicating the status of
            the update.
        """
        if version > self._version:
            self._contents = contents
            self._version = version

            logging.debug('File proxy for {} updated to version {}.'
                          .format(self.filename, self.version))

            return True

        logging.debug('Updating file proxy for {} failed.'
                      .format(self.filename))

        return False

    def get_disk_contents(self):
        """
        :return:
            Returns the contents of a copy of the file
            on the disk. It might not be in sync with
            the editor version of the file.
        """
        with open(self.filename, 'r',
                  encoding=detect_encoding(self.filename)) as disk:
            return disk.read()

    def contents(self):
        """
        :return:
            Returns the current contents of the proxy.
        """
        return self._contents

    def lines(self):
        """
        :return:
            Returns the tuple of lines from the contents
            of current proxy instance.
        """
        # If the file is binary, splitlines returns
        # an empty tuple.
        return tuple(self.contents().splitlines(True))

    def clear(self):
        """
        Clearing a proxy essentially means emptying the
        contents of the proxy instance.
        """
        self._contents = ''
        self._version = -1

    @property
    def filename(self):
        """
        :return:
            Returns the complete normcased file name.
        """
        return self._filename

    @property
    def workspace(self):
        """
        :return:
            Returns the normcased workspace of the file.
        """
        return self._workspace

    @property
    def version(self):
        """
        :return:
            Returns the current edit version of the file.
        """
        return self._version

    @classmethod
    def from_file(cls, filename, workspace, binary=False):
        """
        Construct a FileProxy instance from an existing
        file on the drive.

        :param filename:
            The name of the file to be represented by
            the proxy instance.
        :param workspace:
            The workspace the file belongs to. This can
            be none representing that the the directory
            server is currently serving from is the workspace.
        :return:
            Returns a FileProxy instance of the file with
            the content synced from a disk copy.
        """
        if not binary:
            with open(filename, 'r',
                      encoding=detect_encoding(filename)) as reader:
                return cls(filename, workspace, reader.read())
        else:
            with open(filename, 'rb') as reader:
                return cls(filename, workspace, reader.read())


class FileProxyMap:
    """
    FileProxyMap handles a collection of proxies
    and provides a mechanism to reliably resolve
    missing proxies.

    >>> import tempfile
    >>> file = tempfile.NamedTemporaryFile(delete=False)
    >>> file.write(b'coala')
    5
    >>> file.close()

    You can initialize an empty proxy map using

    >>> proxymap = FileProxyMap()

    Or, you can pass it a list of FileProxy instances
    to build a map from. Addition/Recplacing of a file proxy
    to the map can be done using the add() method and likewise
    deletion can be done using the remove() method. FileProxyMap
    provides a handy function called `resolve()` that can retrive
    a file proxy if it is available in the map or build one for you.

    >>> proxy = proxymap.resolve(file.name, None, binary=False)
    >>> proxy.contents()
    'coala'

    >>> proxy2 = proxymap.resolve(file.name, None)
    >>> proxy.contents()
    'coala'

    >>> proxy == proxy2
    True
    """

    def __init__(self, file_proxies=[]):
        """
        :param file_proxies:
            A list of FileProxy instances to initialize
            the ProxyMap with.
        """
        self._map = {proxy.filename: proxy for proxy in file_proxies}

    @enforce_signature
    def add(self, proxy: FileProxy, replace=False):
        """
        Add a proxy instance to the map or replaces
        optionally if it already exists.

        :param proxy:
            The proxy instance to register in the map.
        :param replace:
            A boolean flag indicating if the proxy should
            replace an existing proxy of the same file.
        :return:
            Boolean true if registering of the proxy was
            successful else false.
        """
        if self._map.get(proxy.filename) is not None:
            if replace:
                self._map[proxy.filename] = proxy
                return True
            return False

        self._map[proxy.filename] = proxy
        return True

    def remove(self, filename):
        """
        Remove the proxy associated with a file from the
        proxy map.

        :param filename:
            The name of the file to remove the proxy
            associated with.
        """
        filename = path.normcase(filename)
        if self.get(filename):
            del self._map[filename]

    def get(self, filename):
        """
        :param filename:
            The name of file to get the associated proxy instance.
        :return:
            A file proxy instance or None if not available.
        """
        filename = path.normcase(filename)
        return self._map.get(filename)

    def resolve(self, filename, workspace=None, hard_sync=True, binary=False):
        """
        Resolve tries to find an available proxy or creates one
        if there is no available proxy for the said file.

        :param filename:
            The filename to search for in the map or to create
            a proxy instance using.
        :param workspace:
            Used in case the lookup fails and a new instance is
            being initialized.
        :hard_sync:
            Boolean flag indicating if the file should be initialized
            from the file on disk or fail otherwise.
        :return:
            Returns a proxy instance or raises associated exceptions.
        """
        filename = path.normcase(filename)

        proxy = self.get(filename)
        if proxy is not None:
            return proxy

        try:
            proxy = FileProxy.from_file(filename, workspace, binary=binary)
        except (OSError, ValueError) as ex:
            if hard_sync:
                raise ex

            # Could raise a ValueError
            proxy = FileProxy(filename, workspace)
            self.add(proxy)

        return proxy


class FileDictGenerator:
    """
    FileDictGenerator is an interface definition class to provide
    structure of a file dict buildable classes.
    """

    def get_file_dict(self, filename_list, *args, **kargs):
        """
        A method to

        :param filename_list: A list of file names as strings to build
                              the file dictionary from.
        :return:              A dict mapping from file names to a tuple
                              of lines of file contents.
        """
        raise NotImplementedError('get_file_dict() needs to be implemented')
