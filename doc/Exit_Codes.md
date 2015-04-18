# Exit Codes

The following is a list of the exit codes and their meanings in the coala code:

 * `0` - coala executed succesfully but yielded no results.
 * `1` - coala executed succesfully but yielded results.
 * `2` - Invalid arguments were passed to coala in the command line.
 * `3` - The file collector exits with this code if an invalid pattern is
   passed to it.
 * `130` - A KeyboardInterrupt (Ctrl+C) was pressed during the execution of
   coala.
 * `255` - Any other general errors.

This list will be updated regularly as and when new exit codes are added to
coala.
