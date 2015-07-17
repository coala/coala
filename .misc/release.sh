#!/bin/bash

set -x
set -e

# Abort if uncommitted things lie around
git diff HEAD --exit-code

# Adjust version number to next release, script will check validity
python3 .misc/adjust_version_number.py coalib/VERSION --new-version ${tag} -b 0

# Commit it
git add coalib/VERSION
git commit -m "[GENERATED] Release ${tag}"

# Put this commit onto master too, rultor doesn't do that by default
git checkout -b tomerge
git checkout master
git merge --ff-only tomerge

# Release!
python3 .misc/adjust_version_number.py coalib/VERSION --release
bash .misc/deploy.pypi.sh
