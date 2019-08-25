import json
try:
    # JSONDecodeError class is available since Python 3.5.x.
    JSONDecodeError = json.decoder.JSONDecodeError
except AttributeError:  # pragma Python 3.5,3.6: no cover
    JSONDecodeError = ValueError

try:
    from asyncio import run_coroutine_threadsafe
except ImportError:  # pragma: no cover
    from coalib.misc.Asyncio import run_coroutine_threadsafe

__all__ = [
    'JSONDecodeError',
    'run_coroutine_threadsafe',
]
