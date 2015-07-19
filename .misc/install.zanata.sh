set -x
set -e

if ./zanata-cli-3.6.0/bin/zanata-cli -v ; then
  export zanata=./zanata-cli-3.6.0/bin/zanata-cli
elif zanata-cli -v ; then
  export zanata=zanata-cli
else
  echo Downloading zanata client...
  wget http://search.maven.org/remotecontent?filepath=org/zanata/zanata-cli/3.6.0/zanata-cli-3.6.0-dist.zip -O zanata-cli-3.6.0-dist.zip -o /dev/null
  echo Unpacking zanata client...
  unzip zanata-cli-3.6.0-dist.zip > /dev/null
  rm zanata-cli-3.6.0-dist.zip
  export zanata=./zanata-cli-3.6.0/bin/zanata-cli
fi

