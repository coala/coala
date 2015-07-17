#!/bin/bash

# Do not use `set -x` here as then it displays the PYPIPW in logs
set -e

# Get environment variables, readily decrypted by rultor
source ../rultor_secrets.sh

# Ship it!
pip3 install twine wheel
python3 setup.py sdist bdist_wheel
twine upload dist/* -u "$PYPIUSER" -p "$PYPIPW"
