import shelve
import time
import platform
import os

class ProjectMetadata:
    def __init__(self):
        self.file = os.path.expanduser('~/.local/.coala')
        if platform.system() == 'windows':# pragma: no cover
            self.file = None
        self.shelf = None

    def add_project(self, name, location):
        self.shelf = shelve.open(self.file)
        timestamp = time.localtime()
        self.shelf[name] = (timestamp, location)
        self.shelf.close()

    def delete_project(self, name):
        self.shelf = shelve.open(self.file)
        del self.shelf[name]
        self.shelf.close()
