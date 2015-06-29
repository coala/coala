set -x
set -e

source .misc/env_variables.sh

if [ "$python_implementation" == "CPython" ] ; then
  python run_tests.py --disallow-test-skipping --cover
else
  python run_tests.py
fi
