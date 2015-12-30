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

This section lists dependencies of coala that are not automatically installed.
On Windows, you can get many with `nuget` (<https://www.nuget.org/>), on Mac
Homebrew will help you installing dependencies (<http://brew.sh/>).

## JS Dependencies

coala features a lot of bears that use linters written in JavaScript. In order
for them to be usable, you need to install them via `npm`
(<http://nodejs.org/>):

```
npm install -g jshint alex remark dockerfile_lint csslint coffeelint
```

If a bear still doesn't work for you, please make sure that you have a decent
version of `npm` installed. Many linux distributions ship a very old one.

## Binary Dependencies

Some bears need some dependencies available:

 * PHPLintBear: Install `php`
 * IndentBear: Install `indent` (be sure to use GNU Indent, Mac ships a non-GNU
   version that lacks some functionality.)
 * CSharpLintBear: Install `mono-mcs`

## Clang

coala features some bears that make use of Clang. In order for them to work, you
need to install libclang:

 * Ubuntu: `apt-get install libclang1`
 * Fedora: `dnf install clang-libs` (Use `yum` instead of `dnf` on Fedora 21 or
   lower.)
 * ArchLinux: `pacman -Sy clang`
 * Windows: `nuget install ClangSharp`
 * OSX: `brew install llvm --with-clang`

If those do not help you, search for a package that contains `libclang.so`.

On windows, you need to execute this command to add the libclang path to the
*PATH* variable permanently (you need to be an administrator):

```setx PATH "%PATH%;%cd%\ClangSharp.XXX\content\x86" \M```

For x86 python or for x64 python:

```setx PATH "%PATH%;%cd%\ClangSharp.XXX\content\x64" \M```

Replace "XXX" with the ClangSharp version you received from nuget.
