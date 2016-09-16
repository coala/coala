set -x
set -e

if python -c "import dbus" ; then
  echo python-dbus already installed
  exit 0
fi

if [ ! -d "dbus-python-1.2.0" ] ; then
  echo Downloading python-dbus...
  # Using -q in wget makes OSX hang sometimes
  wget https://dbus.freedesktop.org/releases/dbus-python/dbus-python-1.2.0.tar.gz -O dbus-python.tar.gz --no-check-certificate
  echo Unpacking python-dbus...
  tar -zxf dbus-python.tar.gz
  rm dbus-python.tar.gz
  cd dbus-python-1.2.0
else
  cd dbus-python-1.2.0
  make clean >/dev/null || make clean
fi

./configure --prefix=$python_virtualenv >/dev/null || ./configure --prefix=$python_virtualenv
make >/dev/null || make
make install >/dev/null || make install

cd ..
