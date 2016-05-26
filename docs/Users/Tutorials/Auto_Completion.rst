Auto completion
===============

If you're using bash or zsh you can setup them to have coala auto command
completion.

Install ``argcomplete``:

::

    $ pip install argcomplete

After this you have to either activate it
`globally <https://github.com/kislyuk/argcomplete#activating-global-completion>`__
or modify your configuration.

If you're using *bash*, add the following to your ``.bashrc``:

::

    eval "$(register-python-argcomplete `which coala`)"

If you're using *zsh*, add the following to your ``.zshrc``:

::

    autoload bashcompinit
    bashcompinit
    eval "$(register-python-argcomplete `which coala`)"

Make sure that coala is added to the PATH at that point. If you want, or you
are unsure if coala is in the PATH, you can replace ```which coala``` with the
path to your coala executable.
