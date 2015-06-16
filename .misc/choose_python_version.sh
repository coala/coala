case $CIRCLE_NODE_INDEX in
 0)
  echo Using Python 3.4.2...
  pyenv install -ks 3.4.2
  pyenv local 3.4.2
  ;;
 2)
  echo Using Python 3.2.5...
  # The python 3.2.5 version that circleci provides by default is UCS2 and not
  # UCS4 - all versions of Python in apt-get and 3.4 and 3.3 of circleci are
  # in UCS4. So, force circleci to regenerate the environment with UCS4.
  # This is needed for any python library compiled from source
  PYTHON_CONFIGURE_OPTS="--with-wide-unicode" pyenv install -kf 3.2.5
  pyenv local 3.2.5
  ;;
 *)
  echo Using Python 3.3.3...
  pyenv install -ks 3.3.3
  pyenv local 3.3.3
  ;;
esac
