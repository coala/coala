import json
try:
    JSONDecodeError = json.decoder.JSONDecodeError
except AttributeError:  # pragma: no cover
    JSONDecodeError = ValueError
