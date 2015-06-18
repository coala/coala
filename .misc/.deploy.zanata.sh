#!/bin/bash

set -e
set -x

cd .misc

echo Getting Zanata API Key...
bash zanata_key.sh

echo Running Zanata...
sh .install.zanata.sh
zanata-cli-3.6.0/bin/zanata-cli -B push --key $ZANATA_KEY --username sils --url https://translate.zanata.org/zanata/
cd ..
