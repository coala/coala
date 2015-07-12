# coala Installation

This document contains information on how to install coala and its
dependencies. Optional dependencies are marked with (*).

> For Windows users:
>
> Some dependencies for Windows are installed via the package-manager *nuget*
> that can be found under https://www.nuget.org/. Be sure to use the
> command-line tool and not the integrated version for Visual Studio.
>
> Note that *nuget* installs all packages into the current working directory.

# Dependencies

## Python
coala requires an installation of Python3 >= 3.2 from http://www.python.org.
coala is fully tested against python versions 3.2, 3.3 and 3.4.

## eSpeak (*)
If you want to use coalas voice outputter you need to install eSpeak from
http://espeak.sourceforge.net/. Note that voice output is currently only
possible when developing for coala. If you care for voice output, please
contact us so we will speed up development of our voice output module.

> For Windows users:
>
> eSpeak is currently not officially supported.

## libclang and munkres
One of the main features of coala is code clone detection. To use it, you need
to install the `libclang` library and the python `munkres` module.

To install libclang:

- Ubuntu 12.04 LTS (least):

  ```apt-get install libclang1```

- Windows:

  You can use the *nuget* package manager to download the `libclang` library:

  ```nuget install ClangSharp```

  And add the libclang path to the *PATH* variable permanently (you need to be
  an administrator):

  ```setx PATH "%PATH%;%cd%\ClangSharp.XXX\content\x86" \M```

  for x86 python or for x64 python:

  ```setx PATH "%PATH%;%cd%\ClangSharp.XXX\content\x64" \M```

  Replace "XXX" with the ClangSharp version you received from nuget.

`munkres` can be installed easily using pip (which is available for both, linux
and Windows):

```pip install munkres```

## gettext (for Windows)
The classic gettext tools that are standard in linux systems are not standard
in Windows systems, so you need to install them manually too if you want to use
translations.

So in your desired installation directory type:

```nuget install Gettext.Tools```

And add the gettext path to the *PATH* variable permanently (you need to be an
administrator):

```setx PATH "%PATH%;%cd%\Gettext.Tools.XXX\tools" \M```

Replace "XXX" with the gettext version you received from nuget.

# coala

coala can be installed afterwards by executing the file setup.py through
the python interpreter:

```python3 setup.py install```

You will have coala installed into your python scripts directory. On an unixoid
system it is probably already available on your command line globally.

Note that the usual installation requires root access. On an unixoid system
(Mac, Linux) this can be achieved by using `sudo`:

```sudo python3 setup.py install```

The easiest way to install under Windows is to start a command prompt as an
administrator and start `setup.py`.

## Alternate installation

If you want to install coala to an alternate location you can e.g. call
`python3 setup.py install --prefix=/your/prefix/location`. Other options are
documented on https://docs.python.org/3.2/install/#alternate-installation.
