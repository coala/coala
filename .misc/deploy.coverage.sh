set -x
set -e

source .misc/env_variables.sh

if [ "$python_implementation" == "CPython" ] ; then
  bash <(curl -s https://codecov.io/bash)
fi
