set -e
# Do not use `set -x` here as then it displays the PYPIPW in circleci logs

if [ "$CIRCLE_BRANCH" = "master" ] ; then
  pip install twine wheel
  python setup.py sdist bdist_wheel
  twine upload dist/* -u "$PYPIUSER" -p "$PYPIPW"
fi
