set -x
set -e

source .misc/env_variables.sh

if [ "$python_implementation" == "CPython" ] ; then
  args=
  if [ "$python_version" == "3.2" ] ; then
    args+="--omit PyLintBearTest"
  fi
  python run_tests.py --disallow-test-skipping --cover -j 1 $args
else
  python run_tests.py -j1
fi
