set -x
set -e

source .misc/env_variables.sh

if [ "$python_implementation" == "CPython" ] ; then
  python run_tests.py --disallow-test-skipping --cover -j3
else
  python run_tests.py -j3
fi
