if python --version | grep 3\.4 && [ "$TRAVIS" = "true" ] ; then
  pip install coveralls codecov
fi

cd .misc

sh .install.python-dbus.sh

cd ..

pip install munkres3

sudo apt-get install espeak libclang1-3.4
