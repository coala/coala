#!/bin/bash

# Do not use `set -x` here as then it displays stuff in logs
set -e

# Get environment variables, readily decrypted by rultor
source ../rultor_secrets.sh

cd .misc
echo Running Zanata...
bash install.zanata.sh
zanata-cli-3.6.0/bin/zanata-cli -B push --key $ZANATA_KEY --username sils --url https://translate.zanata.org/zanata/
cd ..
