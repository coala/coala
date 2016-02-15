set -e
set -x

source .misc/env_variables.sh

args=()

if [ "$system_os" == "LINUX" ] ; then
  args+=('--cov' '--doctest-modules')
fi

python3 -m pytest "${args[@]}"
