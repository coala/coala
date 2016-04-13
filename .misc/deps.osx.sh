set -e
set -x

# Install packages with brew
brew update >/dev/null
brew outdated pyenv || brew upgrade pyenv
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

# Upgrade pip to make sure PEP440 is supported i. e. ~= for versioning
pip install -U pip
# Install packages with pip
pip install -r test-requirements.txt
pip install -r requirements.txt
# Downloading nltk data that's required for nltk to run
bash .misc/deps.nltk.sh
