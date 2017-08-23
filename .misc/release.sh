#!/bin/bash

set -x
set -e

# Abort if uncommitted things lie around
git diff HEAD --exit-code

# Release!
python3 .misc/adjust_version_number.py coalib/VERSION --release
bash .misc/deploy.pypi.sh

# Adjust version number to next release, script will check validity
python3 .misc/adjust_version_number.py coalib/VERSION --new-version ${tag} -b 0

# Commit it
git add coalib/VERSION
git commit -m "[GENERATED] Increment version to ${tag}"
