# coala Installation

This document contains information on how to install coala and its
dependencies. Optional dependencies are marked with (*).

# Dependencies

## Python
coala requires an installation of Python3 >= 3.2 from http://www.python.org.
coala is fully tested against python versions 3.2, 3.3 and 3.4.

## eSpeak (*)
If you want to use coalas voice outputter you need to install eSpeak from
http://espeak.sourceforge.net/. Note that voice output is currently only
possible when developing for coala. If you care for voice output, please
contact us so we will speed up development of our voice output module.

# coala

coala can be installed afterwards by executing the file setup.py through
the python interpreter:

```python3 setup.py install```

You will have coala installed into your python scripts directory. On an unixoid
system it is probably already available on your command line globally.

Note that the usual installation requires root access. On an unixoid system
(Mac, Linux) this can be achieved by using `sudo`:

```sudo python3 setup.py install```

## Alternate installation

If you want to install coala to an alternate location you can e.g. call
`python3 setup.py install --prefix=/your/prefix/location`. Other options are
documented on https://docs.python.org/3.2/install/#alternate-installation.
