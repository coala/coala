set -x
set -e

# Choose the python versions to install deps for
case $CIRCLE_NODE_INDEX in
 0) dep_versions=( "pypy3-2.4.0" "3.2.6" "3.3.6" "3.4.2" ) ;;
 1) dep_versions=( "3.3.6" ) ;;
 2) dep_versions=( "3.2.6" ) ;;
 3) dep_versions=( "pypy3-2.4.0" ) ;;
 *) dep_versions=( "3.4.2" ) ;;
esac

# Install python version needed and related deps

# apt-get commands
sudo apt-get -qq install espeak libclang1-3.4
sudo apt-get -qq install libdbus-glib-1-dev # for python-dbus
sudo apt-get -qq install glib2.0-dev gobject-introspection libgirepository1.0-dev python3-cairo-dev # for python-gi

for dep_version in "${dep_versions[@]}" ; do
  pyenv install -ks $dep_version
  pyenv local $dep_version
  python --version
  source .misc/env_variables.sh

  pip install -q setuptools coverage munkres3

  cd .misc
  if [ "$python_implementation" == "CPython" ] ; then
    bash install.python-gi.sh
    bash install.python-dbus.sh
  fi
  cd ..

done
