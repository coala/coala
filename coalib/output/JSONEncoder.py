import collections
import json
from datetime import datetime

from coalib.misc.Decorators import get_public_members


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "__json__"):
            return obj.__json__()
        elif isinstance(obj, collections.Iterable):
            return list(obj)
        elif isinstance(obj, datetime):
            return obj.isoformat()
        elif hasattr(obj, "__getitem__") and hasattr(obj, "keys"):
            return dict(obj)
        elif hasattr(obj, "__dict__"):
            return {member: getattr(obj, member)
                    for member in get_public_members(obj)}

        return json.JSONEncoder.default(self, obj)
