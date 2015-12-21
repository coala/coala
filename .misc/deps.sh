set -e

# For some reason `nvm` has not been loaded. This generates a lot of output
# in CI, so it's done before `set -x`
if [ -s ~/nvm/nvm.sh ]; then
  source ~/nvm/nvm.sh
  nvm install stable
fi

git -C ~/.pyenv pull

set -x

# Choose the python versions to install deps for
case $CIRCLE_NODE_INDEX in
 0) dep_versions=( "3.5.1" "3.3.6" "3.4.3" ) ;;
 1) dep_versions=( "3.3.6" ) ;;
 2) dep_versions=( "3.5.1" ) ;;
 *) dep_versions=( "3.4.3" ) ;;
esac

# apt-get commands
sudo apt-get -qq update
deps="espeak libclang1-3.4 indent mono-mcs"
deps_python_dbus="libdbus-glib-1-dev libdbus-1-dev"
deps_python_gi="glib2.0-dev gobject-introspection libgirepository1.0-dev python3-cairo-dev"
sudo apt-get -qq install $deps $deps_python_gi $deps_python_dbus

# NPM commands
npm install -g jshint alex mdast dockerfile_lint csslint

for dep_version in "${dep_versions[@]}" ; do
  pyenv install -ks $dep_version
  pyenv local $dep_version
  python --version
  source .misc/env_variables.sh

  pip install -q setuptools coverage munkres3 pylint language-check PyPrint autopep8 eradicate autoflake restructuredtext_lint proselint cpplint

  cd .misc
  bash install.python-gi.sh
  bash install.python-dbus.sh
  cd ..

done

if [ "$CIRCLE_NODE_INDEX" = "0" ] ; then
  pip install -q mkdocs
  pip install -r docs/requirements.txt
fi
