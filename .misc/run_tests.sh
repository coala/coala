case $CIRCLE_NODE_INDEX in
 0)
  python run_tests.py --disallow-test-skipping --cover
  ;;
 1)
  python run_tests.py --disallow-test-skipping
  ;;
 2)
  python run_tests.py --disallow-test-skipping
  ;;
 3)
  python run_tests.py
  ;;
esac
