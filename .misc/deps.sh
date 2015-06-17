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

# Node specific commands
case $CIRCLE_NODE_INDEX in
  0) pip install coveralls codecov ;;
  3) exit 0 ;;
  *) ;;
esac

bash .misc/.install.sh
