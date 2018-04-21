import json
# JSONDecodeError class is available starting from Python 3.5.x.
try:
    # JSONDecodeError class is available since Python 3.5.x.
    JSONDecodeError = json.decoder.JSONDecodeError
except AttributeError:  # pragma Python 3.5,3.6: no cover
    JSONDecodeError = ValueError
