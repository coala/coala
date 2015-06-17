set -x
set -e

# Choose the python versions to install deps for
case $CIRCLE_NODE_INDEX in
 1) dep_version="3.3.3" ;;
 2) dep_version="3.2.5" ;;
 *) dep_version="3.4.2" ;;
esac

if [ $dep_version = "3.2.5" ] ; then
  PYTHON_CONFIGURE_OPTS="--with-wide-unicode" pyenv install -kf $dep_version
else
  pyenv install -ks $dep_version
fi
pyenv local $dep_version

bash .misc/.install.sh
