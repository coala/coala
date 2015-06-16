set -x
set -e

if [ "$TRAVIS_BRANCH" = "master" ] ; then
  sh .misc/.deploy.zanata.sh
fi
