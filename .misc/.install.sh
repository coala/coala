set -x
set -e

cd .misc

sh .install.python-gi.sh
sh .install.python-dbus.sh

cd ..

pip install munkres3
