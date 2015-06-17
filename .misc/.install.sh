set -x
set -e

if [ "$CIRCLECI" = "true" ] ; then
  sudo add-apt-repository -y ppa:fkrull/deadsnakes
  sudo apt-get -qq update
fi

cd .misc

sh .install.python-gi.sh
sh .install.python-dbus.sh

cd ..

pip install munkres3

sudo apt-get -qq install espeak libclang1-3.4
