class ClosableObject:
    def __init__(self):
        self._closed = False

    def _close(self):
        pass

    def close(self):
        if not self._closed:
            self._close()
            self._closed = True
