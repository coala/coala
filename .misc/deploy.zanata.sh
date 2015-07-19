#!/bin/bash

# Do not use `set -x` here as then it displays stuff in logs
set -e

# Get environment variables, readily decrypted by rultor
source ../rultor_secrets.sh

cd .misc
echo Running Zanata...
source install.zanata.sh
$zanata -B push --key $ZANATA_KEY --username sils --url https://translate.zanata.org/zanata/
cd ..
