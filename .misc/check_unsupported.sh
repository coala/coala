#!/usr/bin/env bash

set +e

# Enable capturing the non-zero exit status of coverage instead of tee
set -o pipefail

coverage run setup.py install | tee setup.log

retval=$?

# coalib.__init__.py should exit with 4 on unsupported versions of Python
if [[ $retval != 4 ]]; then
  echo "Unexpected error code $?"

  # When the exit code is 0, use a non-zero exit code instead
  if [[ $retval == 0 ]]; then
    exit 127
  fi
  exit $retval
fi

# error when no lines selected by grep
set -e

grep -q 'coala supports only python 3.4 or later' setup.log

echo "Unsupported check completed successfully"
