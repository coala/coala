sudo apt-get install libdbus-glib-1-dev

if [ "$TRAVIS" = "true" ] ; then
  echo Downloading dbus...
  wget http://dbus.freedesktop.org/releases/dbus/dbus-1.6.30.tar.gz -O dbus.tar.gz -o /dev/null
  echo Unpacking dbus...
  tar -zxvf dbus.tar.gz > /dev/null
  rm dbus.tar.gz

  cd dbus-1.6.30

  ./configure
  make
  sudo make install

  cd ..
fi
