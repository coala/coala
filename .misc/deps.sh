set -e
set -x

# Choose the python versions to install deps for
case $CIRCLE_NODE_INDEX in
 0) dep_versions=( "3.3.6" "3.4.3" "3.5.1" ) ;;
 1) dep_versions=( "3.4.3" ) ;;
 2) dep_versions=( "3.3.6" ) ;;
 *) dep_versions=( "3.5.1" ) ;;
esac

# apt-get commands
sudo apt-get update
deps="espeak indent libclang1-3.4"
deps_python_dbus="libdbus-glib-1-dev libdbus-1-dev"
deps_python_gi="glib2.0-dev gobject-introspection libgirepository1.0-dev python3-cairo-dev"
sudo apt-get install $deps $deps_python_gi $deps_python_dbus

for dep_version in "${dep_versions[@]}" ; do
  pyenv install -ks $dep_version
  pyenv local $dep_version
  python --version
  source .misc/env_variables.sh

  pip install -r test-requirements.txt
  pip install -r requirements.txt

  cd .misc
  bash install.python-gi.sh
  bash install.python-dbus.sh
  cd ..
done

if [ "$CIRCLE_NODE_INDEX" = "0" ] ; then
  pip install -r docs-requirements.txt
fi
