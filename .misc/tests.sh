set -e
set -x

source .misc/env_variables.sh

args=()

if [ "$system_os" == "LINUX" ] ; then
  args+=('--cov' '--cov-fail-under=100' '--doctest-modules')
fi

python3 -m pytest "${args[@]}"
