set -x
set -e

. "$(dirname "$0")"/setup_env_vars.sh
sudo apt-get install ${system_python}-dev libdbus-glib-1-dev

echo Downloading python-dbus...
wget http://dbus.freedesktop.org/releases/dbus-python/dbus-python-1.2.0.tar.gz -O dbus-python.tar.gz -q
echo Unpacking python-dbus...
tar -zxvf dbus-python.tar.gz > /dev/null
rm dbus-python.tar.gz

mkdir -p python-tmpenv

if [ "$CIRCLECI" = "true" ] ; then
  python_virtualenv=`pyenv prefix`
else
  python_virtualenv=$VIRTUAL_ENV
fi

python_tmpenv=`pwd`/python-tmpenv

cd dbus-python-1.2.0

PYTHON=`sudo which ${system_python}` ./configure --prefix=$python_tmpenv
make
make install

cd ..

echo Copying files from the temporary python env to the virtualenv
cp -r $python_tmpenv/* $python_virtualenv
