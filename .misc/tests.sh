set -x
set -e

case $CIRCLE_NODE_INDEX in
 3) python run_tests.py ;;
 *) python run_tests.py --disallow-test-skipping --cover ;;
esac
