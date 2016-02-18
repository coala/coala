set -e
set -x

# Install packages with brew
brew update >/dev/null
brew outdated pyenv || brew upgrade --quiet pyenv
brew install espeak
brew install libffi && brew link libffi --force
brew install cairo
brew install sqlite && brew link sqlite --force
brew install openssl && brew link openssl --force
brew install Py3cairo
brew install d-bus
brew install dbus-glib
brew install gobject-introspection --env=std

# Start dbus in the system
launchctl load -w `find /usr/local/Cellar/d-bus -name "org.freedesktop.dbus-session.plist"`

# Install required python version for this build
pyenv install -ks $PYTHON_VERSION
pyenv global $PYTHON_VERSION
python --version
source .misc/env_variables.sh

# Install packages with pip
pip install -q -r test-requirements.txt
pip install -q -r requirements.txt

# Install packages from source
cd .misc
if [ "$python_implementation" == "CPython" ] ; then
  bash install.python-dbus.sh
fi
cd ..

# Calling setup.py will download checkstyle automatically so tests may succeed
python3 setup.py --help
