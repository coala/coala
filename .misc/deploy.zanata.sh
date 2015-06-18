#!/bin/bash

set -e
set -x

if [ "$CIRCLE_BRANCH" = "master" ] ; then
  cd .misc
  echo Running Zanata...
  bash install.zanata.sh
  zanata-cli-3.6.0/bin/zanata-cli -B push --key $ZANATA_KEY --username sils --url https://translate.zanata.org/zanata/
  cd ..
fi
