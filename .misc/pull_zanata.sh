if [ ! -f ./zanata-cli-3.6.0/bin/zanata-cli ] ; then
  echo Downloading zanata client...
  wget http://search.maven.org/remotecontent?filepath=org/zanata/zanata-cli/3.6.0/zanata-cli-3.6.0-dist.zip -O dist.zip -o /dev/null
  echo Unpacking zanata client...
  unzip dist.zip > /dev/null
  rm dist.zip
fi

echo Pulling translations...
zanata-cli-3.6.0/bin/zanata-cli -B pull --url https://translate.zanata.org/zanata/ > /dev/null

echo Committing translation update...
git add ../locale/*.po
git commit -m "[GENERATED] Update Translations from zanata"

echo Done.
