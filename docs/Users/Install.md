# coala Installation

This document contains information on how to install coala. Supported platforms
are Linux and Windows. coala is known to work on OS X as well. coala is tested
against CPython 3.3, 3.4 and 3.5.

In order to run coala you need to install Python. It is recommended, that
you install Python3 >= 3.3 from http://www.python.org.

The easiest way to install coala is using pip (Pip Installs Packages). If you
don't already have pip, you can install it like described on
<https://pip.pypa.io/en/stable/installing.html>. Note that pip is shipped with
recent python versions by default.

To install the latest most stable version of coala, use:

```
pip3 install coala
```

You can get the latest prerelease version directly from our master branch:

```
pip3 install coala --pre
```

# Installing coala from source

In order to install coala from source, it is recommended to install git. See
<http://git-scm.com/> for further information and a downloadable installer or
use your package manager on linux to get it.

After having git installed, you can download the source code of coala with the
following command:

```
git clone https://github.com/coala-analyzer/coala/
cd coala
```

You can now install coala with a simple:

```
python3 setup.py install
```

You will have coala installed into your python scripts directory. On an unixoid
system it is probably already available on your command line globally.

Note that the usual installation requires root access. On an unixoid system
(Mac, Linux) this can be achieved by using `sudo`:

```
sudo python3 setup.py install
```

The easiest way to install under Windows is to start a command prompt as an
administrator and start `setup.py`.

## Alternate installation

If you want to install coala to an alternate location you can e.g. call
`python3 setup.py install --prefix=/your/prefix/location`. Other options are
documented on <https://docs.python.org/3.3/install/#alternate-installation>.

# Dependencies

This section lists dependencies of coala. All dependencies installable via pip
should already have been installed during the installation of coala and are
not mentioned here.

Optional dependencies are marked with (*).

> **Note**: Installing Dependencies on Windows.
>
> Some dependencies for Windows are installed via the package-manager *nuget*
> that can be found on <https://www.nuget.org/>. Be sure to use the
> command-line tool and not the integrated version for Visual Studio.
>
> Note that *nuget* downloads all packages into the current working directory.

## eSpeak (*)

If you want to use coalas voice outputter you need to install eSpeak from
<http://espeak.sourceforge.net/> or your favorite package manager on linux. Note
that voice output is currently only possible when developing for coala. If
you care for voice output, please contact us so we will speed up development
of our voice output module.

On OSX, espeak can be installed using `brew install espeak`.

> *Note*:
>
> eSpeak is currently unsupported on windows. However it is known to work.

## libclang and munkres (*)

coala features a code clone detection algorithm for clang supported languages.
To use it, you need to install the `libclang` library.

### Linux

To install libclang on linux, we have prepared readily commands for some
distributions for you because this package is hard to find:

 * Ubuntu: `apt-get install libclang1`
 * Fedora: `dnf install clang-libs` (Use `yum` instead of `dnf` on Fedora 21 or
   lower.)
 * ArchLinux: `pacman -Sy clang`

If those do not help you, search for a package that contains `libclang.so`.

### Windows

You can use the *nuget* package manager to obtain the `libclang` library:

```nuget install ClangSharp```

Execute this command to add the libclang path to the *PATH* variable
permanently (you need to be an administrator):

```setx PATH "%PATH%;%cd%\ClangSharp.XXX\content\x86" \M```

For x86 python or for x64 python:

```setx PATH "%PATH%;%cd%\ClangSharp.XXX\content\x64" \M```

Replace "XXX" with the ClangSharp version you received from nuget.

### OSX

This feature is known to work in OSX but is not supported yet.

You can use brew to install clang with `brew install llvm --with-clang`.
