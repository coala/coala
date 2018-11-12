import json
try:
    # JSONDecodeError class is available since Python 3.5.x.
    JSONDecodeError = json.decoder.JSONDecodeError
except AttributeError:  # pragma Python 3.5,3.6: no cover
    JSONDecodeError = ValueError

try:
    # run_coroutine_threadsafe was added in Python 3.4.4
    from asyncio import run_coroutine_threadsafe
    del run_coroutine_threadsafe
    import asyncio
except ImportError:  # pragma: no cover
    from trollius import asyncio

__all__ = [
    'JSONDecodeError',
    'asyncio',
]
