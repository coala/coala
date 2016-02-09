set -e

# For some reason `nvm` has not been loaded. This generates a lot of output
# in CI, so it's done before `set -x`
if [ -s ~/nvm/nvm.sh ]; then
  source ~/nvm/nvm.sh
  nvm use stable
fi

set -x

source .misc/env_variables.sh

args=()

if [ "$python_version" == "3.5" ] ; then
  args+=('-k' 'not PyLintBearTest')
fi
if [ "$system_os" == "LINUX" ] ; then
  args+=('--cov')
fi

python3 -m pytest "${args[@]}"
