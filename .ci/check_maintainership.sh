#!/bin/bash

# Do not use `set -x` here as then it displays the PYPIPW in logs
set -e

# Get environment variables, readily decrypted by rultor
source ../rultor_github_secrets.sh

# Make sure the user is a maintainer
response=$(curl "https://api.github.com/teams/1238757/memberships/${author}?access_token=${GITHUB_TOKEN}")
echo "$response"
if echo "$response" | grep -q "Not Found"; then
    echo "@${author} is not in the maintainers group."
    exit 1
fi
