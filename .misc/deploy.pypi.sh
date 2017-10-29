#!/bin/bash

# Do not use `set -x` here as then it displays the PYPIPW in logs
set -e

# Get environment variables, readily decrypted by rultor
source ../rultor_secrets.sh

# Ship it!
echo "Uploading coala to pypi"
pip3 install twine wheel
python3 setup.py sdist bdist_wheel
# Upload one by one to avoid timeout
twine upload dist/* -u "$PYPIUSER" -p "$PYPIPW" 2>&1 | tee twine_output.txt
if [ "${PIPESTATUS[0]}" -ne 0 ]; then
    SEARCH_STR="500 Server Error"
    if grep -q "$SEARCH_STR" twine_output.txt; then
        echo "Server error 500"
        exit 1
    fi
fi
rm twine_output.txt

echo "Installing coala from pypi"
pip3 install --pre coala==`cat coalib/VERSION` --upgrade
echo coala versions: pip=`coala -v` repo=`cat coalib/VERSION`
[ `coala -v` = `cat coalib/VERSION` ]
