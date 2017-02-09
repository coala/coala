set -e
set -x

export PLATFORM_SYSTEM=$(python -c "import platform; print(platform.system())")
export OS_NAME=$(python -c "import os; print(os.name)")

python -m pytest $*
