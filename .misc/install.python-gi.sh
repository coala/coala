set -x
set -e

echo Downloading python-gi...
wget http://ftp.gnome.org/pub/GNOME/sources/pygobject/3.16/pygobject-3.16.2.tar.xz -O python-gi.tar.xz -q
echo Unpacking python-gi...
tar -xJf python-gi.tar.xz > /dev/null
rm python-gi.tar.xz

cd pygobject-3.16.2

PYTHON=`sudo which ${system_python}` ./configure --prefix=$python_virtualenv
make >/dev/null || make
make install

cd ..
