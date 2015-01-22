class Collector:
    def __init__(self):
        self._items = None

    def collect(self):
        raise NotImplementedError

    def __iter__(self):
        self._assert_item_availability()

        return iter(self._items)

    def __len__(self):
        self._assert_item_availability()

        return len(self._items)

    def __getitem__(self, item):
        self._assert_item_availability()

        return self._items[item]

    def __reversed__(self):
        self._assert_item_availability()

        return reversed(self._items)

    def _assert_item_availability(self):
        if self._items is None:
            raise ValueError("Collector must collect items before they can be accessed")
