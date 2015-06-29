set -x
set -e

source .misc/env_variables.sh

if [ "$python_implementation" == "CPython" ] ; then
  codecov
fi
