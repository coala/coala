set -e

# For some reason `nvm` has not been loaded. This generates a lot of output
# in CI, so it's done before `set -x`
if [ -s ~/nvm/nvm.sh ]; then
  source ~/nvm/nvm.sh
  nvm use stable
fi

set -x

source .misc/env_variables.sh

args="-j1 --timeout 120"

if [ "$python_version" == "3.5" ] ; then
  args+=" --omit PyLintBearTest"
fi
if [ "$system_os" == "LINUX" ] ; then
  args+=" --disallow-test-skipping --cover"
fi

python run_tests.py $args
