README
======
```
                                                     .o88Oo._
                                                    d8P         .ooOO8bo._
                                                    88                  '*Y8bo.
                                      __            YA                      '*Y8b   __
                                    ,dPYb,           YA                        68o68**8Oo.
                                    IP'`Yb            "8D                       *"'    "Y8o
                                    I8  8I             Y8     'YB                       .8D
                                    I8  8P             '8               d8'             8D
                                    I8  8'              8       d8888b          d      AY
     ,gggo,    ,ggggo,    ,gggo,gg  I8 dP    ,gggo,gg   Y,     d888888         d'  _.oP"
    dP"  "Yb  dP"  "Y8go*8P"  "Y8I  I8dP    dP"  "Y8I    q.    Y8888P'        d8
   i8'       i8'    ,8P i8'    ,8I  I8P    i8'    ,8I     "q.  `Y88P'       d8"
  ,d8,_    _,d8,   ,d8' d8,   ,d8b,,d8b,_ ,d8,   ,d8b,       Y           ,o8P
ooP""Y8888PP*"Y8888P"   "Y8888P"`Y88P'"Y88P"Y8888P"`Y8            oooo888P"
```

ABOUT
=====
coala is a simple COde AnaLysis Application. Its goal is to make static code
analysis easy while remaining completely modular and therefore extendable.

Code analysis happens in python scripts while coala manages these, tries to
provide helpful libraries and provides multiple user interfaces. (Currently
we support only Console output but others will follow.)

We are currently working hard to make this project reality. coala is currently
in an alpha stage and provides the most basic features. If you want to see how
the development progresses, check out

https://github.com/coala-analyzer/coala

Authors
-------
Current maintainers and creators are:
Lasse Schuirmann  <lasse@schuirmann.net> and Fabian Neuschmidt <fabian@neuschmidt.de>

Build status
------------
[![Build Status](https://travis-ci.org/coala-analyzer/coala.svg?branch=master)](https://travis-ci.org/coala-analyzer/coala)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/coala-analyzer/coala/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/coala-analyzer/coala/?branch=master)
[![Coverage Status](https://coveralls.io/repos/coala-analyzer/coala/badge.svg)](https://coveralls.io/r/coala-analyzer/coala)

INSTALLATION
============
Python
------
coala requires an installation of Python3 >= 3.2 from http://www.python.org.
coala is fully tested against python versions 3.2, 3.3 and 3.4.

coala
-----
coala can be installed afterwards by executing the file setup.py through
the python interpreter (root access necessary):

```python3 setup.py install```

You will have coala installed into your python scripts directory. On a unix
system it is probably already available on your command line globally.

FUNCTION REFERENCE
==================
Try executing `coala -h` for information about the most common settings. You
can also define settings via the .coafile in the current directory (try the
`--save` option). If a bear needs a setting that is not provided, coala will
explicitly ask you for it.

GETTING INVOLVED
================
We are working hard to make coala reality. If you want to help us you can do
the following things:
- send us an email (see authors above)
- give us feedback
- report bugs
- send pull requests (write objects, tests)
- provide translations

Modularity, clean good code as well as a high usability for both users and
developers of analyse routines (called bears) stand in the foreground of the
development. We will not speed up our development if it needs sacrificing
any aspect of quality.

LICENSE
=======
This program is free software: you can redistribute it and/or modify it under
the terms of the GNU Affero General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more
details.

You should have received a copy of the GNU Affero General Public License along
with this program.  If not, see <http://www.gnu.org/licenses/>.
