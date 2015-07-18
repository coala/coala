#!/bin/bash

set -x
set -e

cd ..
echo '' > locale/coala.pot
echo Generating new pot file...
cat `find coalib/ bears/ -name "*.py"` \
 | python3 .misc/.extract_doc_translations > .doc_strings
xgettext -j -c --language=Python --output=locale/coala.pot --keyword=_ \
 --keyword=N_ --from-code=UTF-8 --package-name=coala \
 --package-version=`./coala --version` \
 --msgid-bugs-address=lasse.schuirmann@gmail.com \
 --copyright-holder="The coala authors" \
 `find coalib/ bears/ -name "*.py"` .doc_strings

echo Removing temporary files...
rm .doc_strings
echo Done.
echo
echo Please update the po files accordingly.
