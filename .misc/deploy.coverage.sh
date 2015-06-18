set -x
set -e

if [ $CIRCLE_NODE_INDEX = 0 ] ; then
  echo Submitting coverage data...
  coveralls
  codecov
fi
