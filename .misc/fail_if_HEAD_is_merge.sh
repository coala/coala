#!/bin/bash

set -e
set -x

if [[ "$(git log --merges HEAD^..)" == "" ]]; then
    exit 0
else
    echo "Not possible to fastforward! Please rebase!"
    exit 1
fi
