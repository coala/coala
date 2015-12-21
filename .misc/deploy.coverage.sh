set -x
set -e

source .misc/env_variables.sh

bash <(curl -s https://codecov.io/bash)
