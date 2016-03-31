Coverage Installation Hints for OSX Users:
==========================================

1. Make sure you have installed Xcode and Homebrew.
---------------------------------------------------

2. Install Python3.
-------------------

::

    $ brew search python  # This should display python3
    $ brew install python3
    $ python3 --version   # To check the installed version

3. Create Virtual environments with pyvenv
------------------------------------------

::

    # Create Virtual Env named myenv
    $ pyvenv myenv

    # This will create a folder named myenv in the
    # current directory. To activate this environment just type
    $ source myenv/bin/activate

    # You can start Python3 by typing:
    $ python

4. Virtualenvwrapper with Python 3:
-----------------------------------

::

    # Installation
    $ pip3 install virtualenv
    $ pip3 install virtualenvwrapper

    # Folder to contain Virtual Environments
    $ mkdir ~/.virtualenvs

    # Add the following in ~/.bash_profile
    $ export WORKON_HOME=~/.virtualenvs
    $ source /usr/local/bin/virtualenvwrapper.sh

    # Activate Changes
    $ source ~/.bash_profile

    # Get Python3 path (python3_pth)
    $ where python3

    # Create a new virtual environment with Python3
    $ mkvirtualenv --python=python3_path myenv

Finally!
--------

::

    # Install python-coverage3 by
    $ easy_install coverage

