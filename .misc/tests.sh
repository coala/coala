set -x
set -e

source .misc/env_variables.sh

if [ "$python_implementation" == "CPython" ] ; then
  python run_tests.py --disallow-test-skipping --cover -j1
else
  python run_tests.py -j1
fi
