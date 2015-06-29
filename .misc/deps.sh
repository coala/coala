set -x
set -e

# Env vars for deps.sh
export python_virtualenv=`pyenv prefix`

# apt-get commands
sudo apt-get -qq install espeak libclang1-3.4
sudo apt-get -qq install libdbus-glib-1-dev # for python-dbus
sudo apt-get -qq install glib2.0-dev gobject-introspection libgirepository1.0-dev python3-cairo-dev # for python-gi

pip install -q setuptools codecov munkres3

cd .misc
bash install.python-gi.sh
bash install.python-dbus.sh
cd ..
