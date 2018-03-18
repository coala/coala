#!/bin/bash

set -e

if [[ ${UNSUPPORTED} == "false" || ${TRAVIS_BRANCH} == "master" ]]; then
    py.test
fi

python setup.py bdist_wheel
pip install ./dist/coala-*.whl
pip install coala-bears[alldeps] --pre -U

# https://github.com/coala/coala-bears/issues/1037
if [[ "$TRAVIS_PULL_REQUEST" != "false" ]]; then
  sed -i.bak '/bears = GitCommitBear/d' .coafile
fi

coala --non-interactive
python setup.py docs
