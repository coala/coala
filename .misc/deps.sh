set -e
set -x

# Choose the python versions to install deps for
case $CIRCLE_NODE_INDEX in
 0) dep_versions=( "3.4.3" "3.5.1" ) ;;
 1) dep_versions=( "3.4.3" ) ;;
 *) dep_versions=( "3.5.1" ) ;;
esac

# apt-get commands
if [ "$CIRCLE_BUILD_IMAGE" = "ubuntu-12.04" ]; then
  sudo add-apt-repository -y ppa:staticfloat/juliareleases
  sudo add-apt-repository -y ppa:staticfloat/julia-deps
fi
sudo apt-get update
deps="indent libclang1-3.4 r-base"
deps_python_dbus="libdbus-glib-1-dev libdbus-1-dev"
deps_python_gi="glib2.0-dev gobject-introspection libgirepository1.0-dev python3-cairo-dev"
deps_ruby_npm="gem nodejs"
deps_julia="julia"
deps_julia_packages="Lint"
sudo apt-get install $deps $deps_python_gi $deps_python_dbus $deps_ruby_npm $deps_julia

for julia_package in $deps_julia_packages ; do
  julia -e 'Pkg.add("'$julia_package'")'
done

for dep_version in "${dep_versions[@]}" ; do
  pyenv install -ks $dep_version
  pyenv local $dep_version
  python --version
  source .misc/env_variables.sh

  pip install -r test-requirements.txt
  pip install -r requirements.txt
  # Downloading nltk data that's required for nltk to run
  bash .misc/deps.nltk.sh

  cd .misc
  bash install.python-gi.sh
  bash install.python-dbus.sh
  cd ..
done

if [ "$CIRCLE_NODE_INDEX" = "0" ] ; then
  pip install -r docs-requirements.txt
fi

# gem installations
gem install ruby
