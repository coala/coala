if [ $CIRCLE_NODE_INDEX = 0 ] ; then
  echo Creating binary distribution...
  python3 setup.py bdist --formats=gztar,zip,rpm
  python3 setup.py sdist --formats=gztar,zip
fi
