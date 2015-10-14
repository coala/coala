set -x
set -e

if python -c "import dbus" ; then
  echo python-dbus already installed
  exit 0
fi

dbus_version=${1:-1.2.0}

if [ ! -d "dbus-python-${dbus_version}" ] ; then
  echo Downloading python-dbus...
  # Using -q in wget makes OSX hang sometimes
  wget http://dbus.freedesktop.org/releases/dbus-python/dbus-python-${dbus_version}.tar.gz
  echo Unpacking python-dbus...
  tar -zxf dbus-python-${dbus_version}.tar.gz
  rm dbus-python-${dbus_version}.tar.gz
  cd dbus-python-${dbus_version}
else
  cd dbus-python-${dbus_version}
  make clean >/dev/null || make clean
fi

./configure --prefix=$python_virtualenv >/dev/null || ./configure --prefix=$python_virtualenv
make >/dev/null || make
make install >/dev/null || make install

cd ..
