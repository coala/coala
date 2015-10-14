set -x
set -e

if python -c "import gi" ; then
  echo python-gi already installed
  exit 0
fi

gi_version=${1:-3.16.2}
gi_major_version=`echo $gi_version | cut -d. -f1-2`

if [ ! -d "pygobject-${gi_version}" ] ; then
  echo Downloading python-gi...
  # Using -q in wget makes OSX hang sometimes
  wget http://ftp.gnome.org/pub/GNOME/sources/pygobject/${gi_major_version}/pygobject-${gi_version}.tar.xz
  echo Unpacking python-gi...
  tar -xJf pygobject-${gi_version}.tar.xz
  rm pygobject-${gi_version}.tar.xz
  cd pygobject-${gi_version}
else
  cd pygobject-${gi_version}
  make clean >/dev/null || make clean
fi

./configure --prefix=$python_virtualenv >/dev/null || ./configure --prefix=$python_virtualenv
make >/dev/null || make
make install >/dev/null || make install

cd ..
