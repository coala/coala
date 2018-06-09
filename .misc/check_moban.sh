#!/bin/bash

set -ex

: "${MOBAN_BRANCH:=master}"

git clone https://gitlab.com/coala/mobans \
          --branch=${MOBAN_BRANCH} ../coala-mobans

moban
git diff --exit-code
