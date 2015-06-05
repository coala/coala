echo Trying to find python version...

python_version=`python -c 'import sys; print(".".join(map(str, sys.version_info[:3])))'`

case "$python_version" in
  "3.4"*)
    system_python=python3.4
    ;;
  "3.3"*)
    system_python=python3.3
    ;;
  "3.2"*)
    system_python=python3.2
    ;;
  *)
    echo Python version was not understood. It was detected as - $python_version
    ;;
esac

if [ "$SCRUTINIZER" = "true" ] ; then
  sudo apt-get install -y software-properties-common
  sudo add-apt-repository -y ppa:fkrull/deadsnakes
  sudo apt-get update
fi
sudo apt-get install -y ${system_python}-dev

sh .install.dbus.sh

echo Downloading python-dbus...
wget http://dbus.freedesktop.org/releases/dbus-python/dbus-python-1.2.0.tar.gz -O dbus-python.tar.gz -o /dev/null
echo Unpacking python-dbus...
tar -zxvf dbus-python.tar.gz > /dev/null
rm dbus-python.tar.gz

mkdir -p python-tmpenv

if [ "$SCRUTINIZER" = "true" ] ; then
  python_virtualenv=${PYENV_ROOT}/versions/$python_version
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
