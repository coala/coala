set -x
set -e

. "$(dirname "$0")"/setup_env_vars.sh

sudo apt-get -qq install ${system_python}-dev glib2.0-dev gobject-introspection libgirepository1.0-dev python3-cairo-dev

echo Downloading python-gi...
wget http://ftp.gnome.org/pub/GNOME/sources/pygobject/3.16/pygobject-3.16.2.tar.xz -O python-gi.tar.xz -q
echo Unpacking python-gi...
tar -xJf python-gi.tar.xz > /dev/null
rm python-gi.tar.xz

cd pygobject-3.16.2

PYTHON=`sudo which ${system_python}` ./configure --prefix=$python_virtualenv
make
make install

cd ..
