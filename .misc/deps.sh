set -x
set -e

# Choose the python versions to install deps for
case $CIRCLE_NODE_INDEX in
 0) dep_versions=( "pypy3-2.4.0" "3.5.0" "3.3.6" "3.4.2" ) ;;
 1) dep_versions=( "3.3.6" ) ;;
 2) dep_versions=( "3.5.0" ) ;;
 3) dep_versions=( "pypy3-2.4.0" ) ;;
 *) dep_versions=( "3.4.2" ) ;;
esac

# apt-get commands
sudo apt-get -qq update
deps="espeak libclang1-3.4 indent"
deps_python_dbus="libdbus-glib-1-dev libdbus-1-dev"
deps_python_gi="glib2.0-dev gobject-introspection libgirepository1.0-dev python3-cairo-dev"
sudo apt-get -qq install $deps $deps_python_gi $deps_python_dbus

# NPM commands
source ~/nvm/nvm.sh # For some reason `nvm` has not been loaded.
nvm install stable
npm install -g jshint alex dockerfile_lint

for dep_version in "${dep_versions[@]}" ; do
  pyenv install -ks $dep_version
  pyenv local $dep_version
  python --version
  source .misc/env_variables.sh

  pip install -q setuptools coverage munkres3 pylint language-check PyPrint autopep8 eradicate autoflake restructuredtext_lint proselint

  if [ "$python_version" = "3.4" ] ; then
    pip install -q mkdocs
    pip install -r docs/requirements.txt
  fi

  cd .misc
  if [ "$python_implementation" == "CPython" ] ; then
    bash install.python-gi.sh
    bash install.python-dbus.sh
  fi
  cd ..

done
