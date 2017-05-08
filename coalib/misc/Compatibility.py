import json
"""
json.decoder.JSONDecodeError gives an AttributeError
because JSONDecodeError missing in Python 3.4

"""
try:
    JSONDecodeError = json.decoder.JSONDecodeError
except AttributeError:  # pragma: no cover
    JSONDecodeError = ValueError
