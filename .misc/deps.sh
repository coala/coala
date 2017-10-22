set -e
set -x

if [[ $CIRCLE_NODE_TOTAL != 2 ]]; then
  echo "ERROR: You must allocate 2 containers for the tests to run properly!"
  exit 1
fi

# Choose the python versions to install deps for
case $CIRCLE_NODE_INDEX in
 0) dep_versions=( "3.4.3" "3.5.1" ) ;;
 1) dep_versions=( "3.4.3" ) ;;
 *) dep_versions=( "3.5.1" ) ;;
esac

# apt-get commands
deps="libclang1-3.4"
sudo apt-get install $deps

for dep_version in "${dep_versions[@]}" ; do
  pyenv install -ks $dep_version
  pyenv local $dep_version
  python --version

  pip install -r test-requirements.txt
  pip install -r requirements.txt
done

if [ "$CIRCLE_NODE_INDEX" = "0" ] ; then
  pip install -r docs-requirements.txt
fi
