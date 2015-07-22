set -x
set -e

# Install pyenv
if ! git -C $PYENV_ROOT pull ; then
  rm -rf $PYENV_ROOT
  git clone https://github.com/yyuu/pyenv.git $PYENV_ROOT
fi
if ! which pyenv ; then
  echo 'eval "$(pyenv init -)"' >> ~/.bashrc
fi

# Fetch python version
pyenv install -ks $PYTHON_VERSION
pyenv global $PYTHON_VERSION
python --version
source .misc/env_variables.sh

# pip install
pip install -q setuptools coverage munkres3 pylint language-check
