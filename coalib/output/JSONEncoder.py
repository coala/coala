import collections
import json
from datetime import datetime


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        new_obj = obj
        if isinstance(obj, collections.Iterable):
            return list(obj)
        elif isinstance(obj, datetime):
            return obj.isoformat()
        elif hasattr(obj, "__getitem__") and hasattr(obj, "keys"):
            return dict(obj)
        elif hasattr(obj, "__dict__"):
            return obj.__dict__

        return json.JSONEncoder.default(self, obj)
