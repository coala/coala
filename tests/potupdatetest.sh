#!/bin/sh

/bin/sh generate_pot.sh
if git diff|grep diff>/dev/null; then
    echo "Please update POT file";
    exit 1;
else
    echo "POT files are up to date."
    exit 0;
fi
