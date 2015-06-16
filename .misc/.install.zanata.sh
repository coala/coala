set -x
set -e

if [ ! -f ./zanata-cli-3.6.0/bin/zanata-cli ] ; then
  echo Downloading zanata client...
  wget http://search.maven.org/remotecontent?filepath=org/zanata/zanata-cli/3.6.0/zanata-cli-3.6.0-dist.zip -O dist.zip -o /dev/null
  echo Unpacking zanata client...
  unzip dist.zip > /dev/null
  rm dist.zip
fi
