if python --version | grep 3\.4 ; then
  coveralls
  codecov

  if [ "$TRAVIS_BRANCH" = "master" ] ; then
    cd .misc
    sh .install.zanata.sh
    zanata-cli-3.6.0/bin/zanata-cli -B push --key $ZANATA_API --username sils --url https://translate.zanata.org/zanata/
  fi
fi
