set -x
set -e

source .misc/env_variables.sh

args="-j1 --timeout 120"

if [ "$python_implementation" == "CPython" ] ; then
  if [ "$python_version" == "3.5" ] || [ "$python_version" == "3.2" ] ; then
    args+=" --omit PyLintBearTest"
  fi
  if [ "$system_os" == "LINUX" ] && [ "$TRAVIS" !=  "true" ] ; then
    args+=" --disallow-test-skipping --cover"
  fi
fi

python run_tests.py $args
