# Compatability

To support pypy (which itself only supports Python 3.2.5) and Python 3.3 and
greater we have a compatability module `coalib.misc.Compatability`. It contains
declarations and other to behave like in Python with version 3.3 or greater.

It follows a list of declarations you should use from the compatability module
when you write code for coala.

# Exceptions

- `FileNotFoundError`
  Used to indicate that a given file was not found. Before Python 3.3 this was
  a general `IOError` for file operations or an `OSError` i.e. when using
  `os.remove`.
  Raising this error manually is not permitted since it unifies more than one
  error. Only use it inside a try-except block.
