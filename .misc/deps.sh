set -x
set -e

# Choose the python versions to install deps for
case $CIRCLE_NODE_INDEX in
 1) dep_version="3.3.3" ;;
 2) dep_version="3.2.5" ;;
 *) dep_version="3.4.2" ;;
esac

# Install python version needed
pyenv install -ks $dep_version
pyenv local $dep_version
source .misc/setup_env_vars.sh
if [ ! "$python_unicode_storage" = "UCS4" ] ; then
  pyenv uninstall -f $dep_version
  PYTHON_CONFIGURE_OPTS="--with-wide-unicode" pyenv install -k $python_version
fi
source .misc/setup_env_vars.sh

# apt-get commands
sudo add-apt-repository -y ppa:fkrull/deadsnakes
sudo apt-get -qq update
sudo apt-get -qq install espeak libclang1-3.4
sudo apt-get -qq install ${system_python}-dev
sudo apt-get -qq install libdbus-glib-1-dev # for python-dbus
sudo apt-get -qq install glib2.0-dev gobject-introspection libgirepository1.0-dev python3-cairo-dev # for python-gi
pip install -q setuptools

# Node specific commands
if [[ "$CIRCLE_NODE_INDEX" != "3" ]] ; then
  pip install -q codecov -r requirements.txt

  cd .misc
  bash install.python-gi.sh
  bash install.python-dbus.sh
  cd ..
fi
