set -e
set -x

# Prerequisites for Go
mkdir $HOME/Go
export GOPATH=$HOME/Go
export GOROOT=/usr/local/opt/go/libexec
export PATH=$PATH:$GOPATH/bin
export PATH=$PATH:$GOROOT/bin

# Install packages with brew
brew update >/dev/null
brew outdated pyenv || brew upgrade --quiet pyenv
brew upgrade --quiet go
brew install espeak
brew install libffi && brew link libffi --force
brew install cairo
brew install sqlite && brew link sqlite --force
brew install openssl && brew link openssl --force
brew install Py3cairo
brew install d-bus
brew install dbus-glib
brew install gobject-introspection --env=std
brew install gnu-indent
brew install go

# Install required go libraries
go get -u github.com/golang/lint/golint
go get -u golang.org/x/tools/cmd/goimports
go get -u sourcegraph.com/sqs/goreturns

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
