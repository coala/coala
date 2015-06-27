set -e
# Do not use `set -x` here as then it displays the PYPIPW in circleci logs

if [ "$CIRCLE_BRANCH" = "master" ] ; then
  echo "[distutils]
  index-servers=pypi
  [pypi]
  repository = https://pypi.python.org/pypi
  username = $PYPIUSER
  password = $PYPIPW" > ~/.pypirc
  echo Deploying coala `coala -v`...
  python setup.py register
  python setup.py sdist upload
  rm ~/.pypirc
fi
