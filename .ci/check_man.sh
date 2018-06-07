#!/bin/bash

set -e

if [ $CIRCLECI ]; then
  sudo apt install man
  export MANPATH=$MANPATH:~/.local/man
elif [ $TRAVIS ]; then
  export MANPATH=$MANPATH:$VIRTUAL_ENV/man
fi

man coala | grep "https://coala.io" > /dev/null 2>&1
