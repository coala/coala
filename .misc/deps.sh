set -x
set -e

source .misc/env_variables.sh

# apt-get commands
sudo apt-get -qq install espeak libclang1-3.4
sudo apt-get -qq install libdbus-glib-1-dev # for python-dbus
sudo apt-get -qq install glib2.0-dev gobject-introspection libgirepository1.0-dev python3-cairo-dev # for python-gi

pip install -q setuptools coverage munkres3

cd .misc
if [ "$python_implementation" == "CPython" ] ; then
  bash install.python-gi.sh
  bash install.python-dbus.sh
fi
cd ..
