set -x
set -e

if [ "$CIRCLECI" = "true" ] && [ $CIRCLE_NODE_INDEX = 3 ]; then
  # Don't install any deps for container 3 in circleci
  exit 0
fi

if python --version | grep 3\.4 && [ "$TRAVIS" = "true" ] ; then
  pip install coveralls codecov
fi

if [ "$CIRCLECI" = "true" ] ; then
  sudo add-apt-repository -y ppa:fkrull/deadsnakes
  sudo apt-get update
fi

cd .misc

sh .install.python-dbus.sh

cd ..

pip install munkres3

sudo apt-get install espeak libclang1-3.4
