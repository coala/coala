set -x
set -e

if [ "$TRAVIS_BRANCH" = "master" ] ; then
  cd .misc
  sh .install.zanata.sh
  zanata-cli-3.6.0/bin/zanata-cli -B push --key $ZANATA_API --username sils --url https://translate.zanata.org/zanata/
fi
