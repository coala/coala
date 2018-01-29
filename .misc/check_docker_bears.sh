#!/usr/bin/env bash

set -e -x

# Use the script defined by the docker to run tests,
# as it handles bears which are not supported in the image.
DOCKER_RAW_REPO="https://raw.githubusercontent.com/coala/docker-coala-base"
BRANCH_GUESSER="$DOCKER_RAW_REPO/master/guess_branch.py"

wget "$BRANCH_GUESSER"

if [[ -z "$DOCKER_REPO" ]]; then
  DOCKER_REPO=coala/base
  echo "DOCKER_REPO not set; using $DOCKER_REPO"
fi

if [[ -z "$SOURCE_BRANCH" ]]; then
  if [[ -n "$TRAVIS" ]]; then
    SOURCE_BRANCH="$TRAVIS_BRANCH"
    echo "SOURCE_BRANCH not set; using TRAVIS_BRANCH ($TRAVIS_BRANCH)"
  else
    echo "SOURCE_BRANCH not set"
  fi
fi

COALA_BRANCH=$(python guess_branch.py "$SOURCE_BRANCH")

DOCKER_TESTS="$DOCKER_RAW_REPO/$COALA_BRANCH/tests/pytest.sh"
wget "$DOCKER_TESTS"
chmod 755 pytest.sh

if [[ "$COALA_BRANCH" == "master" ]]; then
  DOCKER_TAG="pre"
elif [[ "${COALA_BRANCH:0:8}" == "release/" ]]; then
  DOCKER_TAG="${COALA_BRANCH:8}"
else
  DOCKER_TAG="$COALA_BRANCH"
fi

IMAGE_NAME="$DOCKER_REPO:$DOCKER_TAG"

# Use the checked out coala, with latest coala-bears for the branch
docker run -t -i --volume="$(pwd):/coala" "$IMAGE_NAME" /bin/sh -c "
  set -e -x;
  pip3 install -U /coala/;
  cd /coala-bears;
  git pull;
  python3 setup.py install;
  /coala/pytest.sh;
"
