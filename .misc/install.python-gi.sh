set -x
set -e

if python -c "import gi" ; then
  echo python-gi already installed
  exit 0
fi

if [ ! -d "pygobject-3.16.2" ] ; then
  echo Downloading python-gi...
  # Using -q in wget makes OSX hang sometimes
  wget http://ftp.gnome.org/pub/GNOME/sources/pygobject/3.16/pygobject-3.16.2.tar.xz -O python-gi.tar.xz
  echo Unpacking python-gi...
  tar -xJf python-gi.tar.xz
  rm python-gi.tar.xz
  cd pygobject-3.16.2
else
  cd pygobject-3.16.2
  make clean >/dev/null || make clean
fi

./configure --prefix=$python_virtualenv >/dev/null || ./configure --prefix=$python_virtualenv
make >/dev/null || make
make install >/dev/null || make install

cd ..
