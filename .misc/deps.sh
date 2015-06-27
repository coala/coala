set -x
set -e

# Choose the python versions to install deps for
case $CIRCLE_NODE_INDEX in
 1) dep_version="3.3.6" ;;
 2) dep_version="3.2.6" ;;
 *) dep_version="3.4.2" ;;
esac

# Install python version needed
# Note - `--with-wide-unicode` is needed only because 3.2.5 defaults to UCS2 unicode
PYTHON_CONFIGURE_OPTS="--with-wide-unicode" pyenv install -ks $dep_version
pyenv local $dep_version
source .misc/setup_env_vars.sh
if [ ! "$python_unicode_storage" = "UCS4" ] ; then
  pyenv uninstall -f $dep_version
  PYTHON_CONFIGURE_OPTS="--with-wide-unicode" pyenv install -k $python_version
  source .misc/setup_env_vars.sh
fi

# apt-get commands
sudo apt-get -qq install espeak libclang1-3.4
sudo apt-get -qq install libdbus-glib-1-dev # for python-dbus
sudo apt-get -qq install glib2.0-dev gobject-introspection libgirepository1.0-dev python3-cairo-dev # for python-gi
pip install -q setuptools

# Node specific commands
if [[ "$CIRCLE_NODE_INDEX" != "3" ]] ; then
  pip install -q codecov munkres3

  cd .misc
  bash install.python-gi.sh
  bash install.python-dbus.sh
  cd ..
fi
